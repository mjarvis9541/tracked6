import datetime
from django.utils import timezone
from django.http import Http404
from diaries.models import Diary


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