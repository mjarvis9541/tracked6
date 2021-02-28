from django.db import models
from django.db.models import (
    Avg,
    Case,
    ExpressionWrapper,
    F,
    Func,
    Sum,
    Value,
    When,
    Window,
)
from django.db.models.functions import Coalesce, Concat, Round

from profiles.models import Profile


class Round1(Func):
    """ Postgres specific database function to round floating point numbers to 1 decimal place """

    function = 'ROUND'
    template = '%(function)s(%(expressions)s::numeric, 1)'


class Round2(Func):
    """ Postgres specific database function to round floating point numbers to 2 decimal places """

    function = 'ROUND'
    template = '%(function)s(%(expressions)s::numeric, 2)'


class DiaryQuerySet(models.QuerySet):
    def summary(self):
        """
        Gets a summary of calculates food values to display on the user's food diary display page.
        """
        return self.select_related('food', 'food__brand').annotate(
            food_name=F('food__name'),
            brand_name=F('food__brand__name'),
            data_value=ExpressionWrapper(
                F('quantity') * F('food__data_value'),
                output_field=models.DecimalField(),
            ),
            data_measurement=F('food__data_measurement'),
            data_value_measurement=Case(
                # removes 'servings' measurement so it's displayed as '1 <item>' instead of '1 serving <item>'
                When(data_measurement='g', then=Value('g')),
                When(data_measurement='ml', then=Value('ml')),
                When(data_measurement='srv', data_value__gt=1, then=Value(' Servings')),
                When(data_measurement='srv', data_value__lte=1, then=Value(' Serving')),
                default=Value(''),
                output_field=models.CharField(),
            ),
            energy=ExpressionWrapper(F('quantity') * F('food__energy'), output_field=models.IntegerField()),
            fat=F('quantity') * F('food__fat'),
            saturates=F('quantity') * F('food__saturates'),
            carbohydrate=F('quantity') * F('food__carbohydrate'),
            sugars=F('quantity') * F('food__sugars'),
            fibre=F('quantity') * F('food__fibre'),
            protein=F('quantity') * F('food__protein'),
            salt=F('quantity') * F('food__salt'),
            sodium=F('salt') * 400,
        )

    def total(self):
        """
        Calculates the total calories and macronutrients for the diary display page.
        """
        return self.summary().aggregate(
            total_energy=Coalesce(Sum('energy'), 0),
            total_fat=Coalesce(Sum('fat'), 0),
            total_saturates=Coalesce(Sum('saturates'), 0),
            total_carbohydrate=Coalesce(Sum('carbohydrate'), 0),
            total_sugars=Coalesce(Sum('sugars'), 0),
            total_fibre=Coalesce(Sum('fibre'), 0),
            total_protein=Coalesce(Sum('protein'), 0),
            total_salt=Coalesce(Sum('salt'), 0),
            total_sodium=Coalesce(Sum('sodium'), 0),
        )

    def remaining(self, user):
        """
        Calculates the remaining calories and macronutrients for the diary
        display page, based off the current user's dietary target.
        """
        total = self.filter(user=user).total()
        target = (
            Profile.objects.filter(user=user)
            .annotate(sodium=ExpressionWrapper(F('salt') * 400, output_field=models.IntegerField()))
            .values()
            .first()
        )
        return {
            'energy': target.get('energy', 0) - total.get('total_energy', 0),
            'fat': target.get('fat', 0) - total.get('total_fat', 0),
            'saturates': target.get('saturates', 0) - total.get('total_saturates', 0),
            'carbohydrate': target.get('carbohydrate', 0) - total.get('total_carbohydrate', 0),
            'sugars': target.get('sugars', 0) - total.get('total_sugars', 0),
            'fibre': target.get('fibre', 0) - total.get('total_fibre', 0),
            'protein': target.get('protein', 0) - total.get('total_protein', 0),
            'salt': target.get('salt', 0) - total.get('total_salt', 0),
            'sodium': target.get('sodium', 0) - total.get('total_sodium', 0),
        }

    def custom_summary(self, macro_1='protein', macro_2='carbohydrate', macro_3='fat'):
        return self.select_related('food').annotate(
            name=F('food__name'),
            brand=F('food__brand'),
            data_value=ExpressionWrapper(
                F('quantity') * F('food__data_value'),
                output_field=models.DecimalField(),
            ),
            data_measurement=F('food__data_measurement'),
            data_value_measurement=Case(
                # removes 'servings' measurement so it's displayed as '1 <item>' instead of '1 serving <item>'
                When(data_measurement='g', then=Value('g')),
                When(data_measurement='ml', then=Value('ml')),
                default=Value(''),
                output_field=models.CharField(),
            ),
            energy=ExpressionWrapper(F('quantity') * F('food__energy'), output_field=models.IntegerField()),
            macro_1=F('quantity') * F(f'food__{macro_1}'),
            macro_2=F('quantity') * F(f'food__{macro_2}'),
            macro_3=F('quantity') * F(f'food__{macro_3}'),
        )
