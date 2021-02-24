import datetime

from django.http import Http404
from django.utils import timezone

from diaries.models import Diary


# class DateMixin:
    # """
    # Validates date parameters that are passed into the url, and provides date information to the context.
    # """
    # date = None
    # previous_day = None
    # next_day = None
    # today = timezone.now()

    # def get_date(self, *args, **kwrags):
    #     year = self.kwargs.get('year', timezone.now().year)
    #     month = self.kwargs.get('month', timezone.now().month)
    #     day = self.kwargs.get('day', timezone.now().day)
    #     try:
    #         self.date = datetime.date(year, month, day)
    #     except ValueError as e:
    #         raise Http404(e)
    #     return
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['date'] = self.date
    #     context['previous_day'] = self.date - datetime.timedelta(days=1)
    #     context['next_day'] = self.date + datetime.timedelta(days=1)
    #     context['today'] = self.today
    #     return context

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


class DateMixin2:
    """
    Requires context mixin to be passed into view if using standard view.
    """
    year = None
    month = None
    day = None
    date = None

    def get_date(self, *args, **kwargs):
        self.year = self.kwargs.get('year', timezone.now().year)
        self.month = self.kwargs.get('month', timezone.now().month)
        self.day = self.kwargs.get('day', timezone.now().day)
        try:
            self.date = datetime.date(self.year, self.month, self.day)
        except Exception:
            raise Http404('Invalid date')
       # By default returns none - just adds to class attrs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_date()
        context['date'] = self.date
        context['previous_day'] = self.date - datetime.timedelta(days=1)
        context['next_day'] = self.date + datetime.timedelta(days=1)
        context['today'] = timezone.now()
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