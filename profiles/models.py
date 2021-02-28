from decimal import Decimal
from django.conf import settings
from django.core.checks import messages
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from utils.behaviours import Nutritionable, Uuidable
from django.urls import reverse
from django.core.validators import MaxValueValidator
from datetime import date
from progress.models import Progress
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

admin_user = get_user_model().objects.get(username='admin')


class Profile(Uuidable):
    """
    Model to store all information about a user. Mainly stats, goals and targets.
    """

    class Sex(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')

    class ActivityLevel(models.TextChoices):
        SEDENTARY = 'SD', _('Sedentary')
        LIGHTLY_ACTIVE = 'LA', _('Lightly Active')
        MODERATELY_ACTIVE = 'MA', _('Moderately Active')
        VERY_ACTIVE = 'VA', _('Very Active')
        EXTRA_ACTIVE = 'EA', _('Extra Active')

    class Goal(models.TextChoices):
        LOSE_WEIGHT = 'LW', _('Lose Fat')
        MAINTAIN_WEIGHT = 'MW', _('Maintain Weight')
        GAIN_WEIGHT = 'GW', _('Build Muscle')

    class CalculationMethod(models.TextChoices):
        RECOMMENDED = 'REC', _('Recommended')
        PERCENT = 'PER', _('Percent')
        GRAMS = 'GRA', _('Grams')
        CUSTOM = 'CUS', _('Custom')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name='profile picture',
        upload_to='images/profile_pictures',
        default='images/profile_pictures/default.png',
        null=True,
        blank=True,
    )

    # Base user stats
    sex = models.CharField(max_length=1, choices=Sex.choices, null=True, blank=True)
    height = models.IntegerField('height (cm)', null=True, blank=True)
    weight = models.DecimalField(
        'weight (kg)', max_digits=4, decimal_places=1, null=True, blank=True
    )
    date_of_birth = models.DateField(
        null=True, blank=True, validators=[MaxValueValidator(limit_value=date.today)]
    )
    activity_level = models.CharField(
        max_length=2,
        choices=ActivityLevel.choices,
        null=True,
        blank=True,
        help_text="""
        <ul>
        <li>Sedentary - Little to no exercise.</li>
        <li>Light Activity - Exercise 1 to 2 days a week.</li>
        <li>Moderate Activity - Exercise 3 to 5 days a week.</li>
        <li>High Activity - Exercise 6 to 7 days a week.</li>
        <li>Very High Activity - Exercise 6 to 7 days a week, and a physical job.</li>
        </ul>
        """,
    )

    # Goals
    goal_weight = models.DecimalField(
        'goal weight (kg)',
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text='Set a goal weight and we\'ll estimate how long it\'ll take for you to reach it.',
    )
    goal = models.CharField(
        max_length=2,
        choices=Goal.choices,
        null=True,
        blank=True,
        help_text="""
        <ul>
        <li>Lose Fat.</li>
        <li>Maintain Weight.</li>
        <li>Gain Muscle.</li>
        </ul>
        """,
    )

    # Targets - defaults taken from recommanded calorie/macronutrient intake for an adult female
    calculation_method = models.CharField(
        max_length=3,
        choices=CalculationMethod.choices,
        null=True,
        blank=True,
        editable=False,
        help_text="Records the method that was used to set the user's macronutrient targets.",
    )
    energy = models.IntegerField(verbose_name='energy (kcal)', default=2000)
    fat = models.DecimalField(
        verbose_name='fat (g)', max_digits=4, decimal_places=1, default=70
    )
    saturates = models.DecimalField(
        verbose_name='saturates (g)', max_digits=4, decimal_places=1, default=20
    )
    carbohydrate = models.DecimalField(
        verbose_name='carbohydrate (g)', max_digits=4, decimal_places=1, default=260
    )
    sugars = models.DecimalField(
        verbose_name='sugars (g)', max_digits=4, decimal_places=1, default=90
    )
    fibre = models.DecimalField(
        verbose_name='fibre (g)', max_digits=4, decimal_places=1, default=30
    )
    protein = models.DecimalField(
        verbose_name='protein (g)', max_digits=4, decimal_places=1, default=50
    )
    salt = models.DecimalField(
        verbose_name='salt (g)', max_digits=5, decimal_places=2, default=6
    )

    __original_weight = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_weight = self.weight

    def save(self, *args, **kwargs):
        # When the user updates their weight, this will either create
        # or update an entry in the progress model with the current date.
        if self.weight != self.__original_weight:
            post = Progress.objects.filter(user=self.user, date=timezone.now()).first()
            if post:
                post.weight = self.weight
                post.save()
                print('updated user weight within progress model on this date')
            else:
                Progress.objects.create(
                    user=self.user, date=timezone.now(), weight=self.weight
                )
                print('created user weight within progress within on this date')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profiles:profile")

    @property
    def sodium(self):
        # Calculates sodium from salt
        if self.salt is not None:
            return round(self.salt * 400)

    # Basic calculations / properties

    @property
    def weight_lb(self):
        # Converts users weight from kg to lb
        if self.weight:
            return round(self.weight * 2.20462)

    @property
    def goal_weight_lb(self):
        # Converts users weight from kg to lb
        if self.goal_weight:
            return round(self.goal_weight * 2.20462)

    @property
    def weight_st(self):
        # Converts users weight from kg to st and lb
        if self.weight_lb:
            weight = {}
            weight['st'] = round(self.weight_lb // 14)
            weight['lb'] = round(self.weight_lb % 14)
            return weight

    @property
    def goal_weight_st(self):
        # Converts users goal weight from kg to st and lb
        if self.goal_weight_lb:
            weight = {}
            weight['st'] = round(self.goal_weight_lb // 14)
            weight['lb'] = round(self.goal_weight_lb % 14)
            return weight

    @property
    def height_in(self):
        # Converts users height from cm to in
        if self.height:
            return round(self.height / 2.54)

    @property
    def height_ft(self):
        # Converts users height from cm to ft and in
        if self.height_in:
            height = {}
            height['ft'] = round(self.height_in // 12)
            height['in'] = round(self.height_in % 12)
            return height

    @property
    def age(self):
        # Calculates users current age based on their date of birth 
        if self.date_of_birth:
            now = timezone.now()
            return (
                now.year
                - self.date_of_birth.year
                - (
                    (now.month, now.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
                )
            )

    @property
    def goal_duration_weeks(self):
        # Calculates how long it will reasonably take the user to go
        # from their current weight to their goal weight (in weeks).
        if self.weight:
            duration = {}
            duration['short'] = abs(self.weight - self.goal_weight) / 1
            duration['long'] = abs(self.weight - self.goal_weight) / 0.5
            return duration

    # Calculations for BMI, BMR and TDEE
    @property
    def bmi(self):
        # Body Mass Index
        if self.weight and self.height:
            return round(self.weight / Decimal(((self.height / 100) ** 2)), 1)

    @property
    def bmr(self):
        # Basal Metablic Rate
        # Calculated using the Harris–Benedict Equation, revised by Mifflin and St Jeor
        if self.weight and self.height:
            modifier = 0
            if self.sex == self.Sex.MALE:
                modifier = 5
            elif self.sex == self.Sex.FEMALE:
                modifier = -161
            return round(
                (10 * self.weight)
                + Decimal(6.25 * self.height)
                - (5 * self.age)
                + modifier
            )

    @property
    def tdee(self):
        # Total Daily Energy Expenditure
        if self.activity_level and self.bmr:
            modifier = 0
            if self.activity_level == self.ActivityLevel.SEDENTARY:
                modifier = 1.2
            elif self.activity_level == self.ActivityLevel.LIGHTLY_ACTIVE:
                modifier = 1.375
            elif self.activity_level == self.ActivityLevel.MODERATELY_ACTIVE:
                modifier = 1.55
            elif self.activity_level == self.ActivityLevel.VERY_ACTIVE:
                modifier = 1.725
            elif self.activity_level == self.ActivityLevel.EXTRA_ACTIVE:
                modifier = 1.9
            return round(self.bmr * modifier)
    
    @property
    def recommended_calories(self):
        # Sets the users recommended calorie target based on their 
        # tdee and goals.
        if self.goal and self.tdee:
            modifier = 0
            if self.goal == self.Goal.LOSE_WEIGHT:
                modifier = 0.8
            elif self.goal == self.Goal.MAINTAIN_WEIGHT:
                modifier = 1
            elif self.goal == self.Goal.GAIN_WEIGHT:
                modifier = 1.1
            return round(self.tdee * modifier)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Creates and links a profile when a user is created.
    if created:
        Profile.objects.create(user=instance)
    if not Profile.objects.filter(user=instance):
        Profile.objects.create(user=instance)
    instance.profile.save()