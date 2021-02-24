from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from utils.behaviours import Nutritionable, Uuidable
from django.urls import reverse

User = settings.AUTH_USER_MODEL

admin_user = get_user_model().objects.get(username='admin')


class Profile(Uuidable):
    class Sex(models.TextChoices):
        MALE = 'M', ('Male')
        FEMALE = 'F', ('Female')

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='images', null=True, blank=True) # default='images/default.jpg'

    # Base user stats    
    sex = models.CharField(max_length=1, choices=Sex.choices, null=True, blank=True)
    height = models.IntegerField('height (cm)', null=True, blank=True)
    weight = models.DecimalField('weight (kg)', max_digits=4, decimal_places=1, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    goal_weight = models.DecimalField('goal weight (kg)', max_digits=4, decimal_places=1, null=True)
    
    # Dietary targets - defaults taken from recommanded average intake for adults
    # won't pull from Nutritionable as we need a default here for new users who haven't set their targets
    energy = models.IntegerField(verbose_name='energy (kcal)', default=2000)
    fat = models.DecimalField(max_digits=4, decimal_places=1, default=70)
    saturates = models.DecimalField(max_digits=4, decimal_places=1, default=20)
    carbohydrate = models.DecimalField(max_digits=4, decimal_places=1, default=260)
    sugars = models.DecimalField(max_digits=4, decimal_places=1, default=90)
    fibre = models.DecimalField(max_digits=4, decimal_places=1, default=30)
    protein = models.DecimalField(max_digits=4, decimal_places=1, default=50)
    salt = models.DecimalField(max_digits=5, decimal_places=2, default=6)


    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    if not Profile.objects.filter(user=instance):
        Profile.objects.create(user=instance)
    instance.profile.save()