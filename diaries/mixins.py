import datetime

from django.http import Http404
from django.utils import timezone
from django.views.generic.base import ContextMixin

from diaries.models import Diary
from food.forms import FoodFilterForm
from food.models import Food



class FoodFilterMixin(ContextMixin):
    """
    Provides the user the ability to filter the food list.
    """
    def filter_queryset(self):
        queryset = Food.objects.summary().values()
        q = self.request.GET.get('q')
        brand = self.request.GET.get('brand')
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort')
        if q:
            queryset = queryset.filter(name__icontains=q)
        if brand:
            try:
                queryset = queryset.filter(brand=brand)
            except Exception:
                raise Http404('Invalid brand filter choice')
        if category:
            try:
                queryset = queryset.filter(category=category)
            except Exception:
                raise Http404('Invalid category filter choice')
        if sort:
            try:
                queryset = queryset.order_by(sort)
            except Exception:
                raise Http404('Invalid sort filter choice')
        return queryset

    def get_context_data(self, **kwargs):
        """Insert filter form into the context dict."""
        queryset = self.filter_queryset()
        kwargs['queryset'] = queryset
        kwargs['form'] = FoodFilterForm(self.request.GET)
        return super().get_context_data(**kwargs)


class DiaryDateMixin(ContextMixin):
    """
    Validates date parameters if passed into url paramters, else returns todays date.
    Adds the date, previous day, next day and today to the context dictionary.
    """

    # year = None
    # month = None
    # day = None
    # today = None
    # date = None

    def get_diary_date(self, *args, **kwargs):
        year = self.kwargs.get('year', timezone.now().year)
        month = self.kwargs.get('month', timezone.now().month)
        day = self.kwargs.get('day', timezone.now().day)

        try:
            self.date = datetime.date(year, month, day)
            self.previous_day = self.date - datetime.timedelta(days=1)
            self.next_day = self.date + datetime.timedelta(days=1)
            self.today = timezone.now()
        except Exception:
            raise Http404('Invalid date. Must be in format YYYY-MM-DD.')

    def get_context_data(self, **kwargs):
        """Insert dates into the context dict."""
        self.get_diary_date()
        kwargs['date'] = self.date
        kwargs['previous_day'] = self.previous_day
        kwargs['next_day'] = self.next_day
        kwargs['today'] = self.today
        return super().get_context_data(**kwargs)


class DiaryMealMixin(ContextMixin):
    """
    Validates meal number passed into url params.
    Adds the meal number and meal name to the context dictionary.
    """

    # diary_meal = None
    # diary_meal_name = None

    def get_diary_meal(self, *args, **kwargs):

        meal = self.kwargs.get('meal')
        if meal not in range(1, 7):
            raise Http404('Invalid diary meal number provided within the URL. Diary meal number must be between 1 and 6.')

        self.diary_meal = meal
        self.diary_meal_name = [x[1] for x in Diary.Meal.choices if x[0] == meal][0]

    def get_context_data(self, **kwargs):
        """ Inserts meal information into context dict."""
        self.get_diary_meal()
        kwargs['meal'] = self.diary_meal
        kwargs['meal_name'] = self.diary_meal_name
        return super().get_context_data(**kwargs)




""" To Remove """

class MealMixin:
    """
    Mixin that validates the meal passed into the URL params is a valid choice.
    Provides the meal name to the view.
    """

    meal = None
    meal_name = None
    meal_num = None

    def dispatch(self, request, *args, **kwargs):
        if not self.kwargs['meal'] in range(1, 7):
            raise Http404('Invalid meal')
        else:
            self.meal = self.kwargs['meal']
            self.meal_name = [x[1] for x in Diary.Meal.choices if x[0] == self.meal][0]
            self.meal_num = self.meal
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_name'] = self.meal_name
        context['meal_num'] = self.meal_num
        return context


class DateMixin:
    """
    Mixin that validates the date passed into the URL by the user.
    Adds date object, next and previous days to the context dictionary.
    """

    date = None
    previous_day = None
    next_day = None
    today = timezone.now()

    def dispatch(self, request, *args, **kwargs):
        year = self.kwargs.get('year', timezone.now().year)
        month = self.kwargs.get('month', timezone.now().month)
        day = self.kwargs.get('day', timezone.now().day)
        try:
            self.date = datetime.date(year, month, day)
        except ValueError as e:
            raise Http404(e)  # raise Http404('Invalid date')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = self.date
        context['previous_day'] = self.date - datetime.timedelta(days=1)
        context['next_day'] = self.date + datetime.timedelta(days=1)
        context['today'] = self.today
        return context
