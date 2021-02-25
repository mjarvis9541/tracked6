from django.shortcuts import render
from django.views.generic import View
# from django.views.generic.base import ContextMixin

# # Example templateview for adding post
# from django.views.generic import TemplateView

# class TemplatePostView(TemplateView):
#     template_name = 'profiles/profile.html'

#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context)

# class BaseView(ContextMixin, View):
#     """
#     Provides a default get/post request that renders a response with the given template name.
#     """
#     template_name = None

#     def get(self, request):
#         return render(request, self.template_name, self.context)

#     def post(self, request):
#         return render(request, self.template_name, self.context)

import datetime
from django.http import Http404
from diaries.models import Diary
from django.utils import timezone
from .models import Profile
from django.contrib import messages
from diaries.forms import DiaryUpdateForm


class DateMixin:
    def get_year(self):
        """Return the year for which this view should display data."""
        year = self.year
        if year is None:
            try:
                year = self.kwargs['year']
            except KeyError:
                try:
                    year = self.request.GET['year']
                except KeyError:
                    raise Http404('No year specified')
        return year
                
    def get_month(self):
        """Return the month for which this view should display data."""
        month = self.month
        if month is None:
            try:
                month = self.kwargs['month']
            except KeyError:
                try:
                    month = self.request.GET['month']
                except KeyError:
                    raise Http404('No month specified')
        return month

    def get_day(self):
        """Return the day for which this view should display data."""
        day = self.day
        if day is None:
            try:
                day = self.kwargs['day']
            except KeyError:
                try:
                    day = self.request.GET['day']
                except KeyError:
                    raise Http404('No day specified')
        return day


class ContextMixin:
    """
    A default context mixin that passes the keyword arguments received by
    get_context_data() as the template context.
    """
    
    extra_context = None
    
    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs


class DateMixin:
    date = timezone.now()

    def get_date(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        try:
            self.date = datetime.date(year, month, day)
        except ValueError as e:
            raise Http404(e)
    
    def get_my_context(self, **kwargs):
        # for this to work in the view, this DateMixin needs to come first... MRO left.
        context = super().get_my_context(**kwargs)
        self.get_date()
        context['date'] = self.date
        context['day'] = self.day
        return context
    

class MealMixin:
    """
    Validates the meal number that's passed into the url params.
    Returns the meal name
    """
    meal_number = None
    meal_name = None 

    def get_meal(self):
        self.meal = self.kwargs.get('meal')
        self.meal_name = self.meal_name = [x[1] for x in Diary.Meal.choices if x[0] == self.meal][0]


from food.forms import FoodFilterForm


class ProfileView(View):
    template_name = 'profiles/profile.html'
    context = {}


    def get_year(self):
        month = self.kwargs.get('month', timezone.now().month)
        self.context['month'] = month
        return month

        
    def get_month(self):
        month = self.kwargs.get('month', timezone.now().month)
        self.context['month'] = month
        return month

    def get_day(self):
        day = self.kwargs.get('day', timezone.now().day)
        self.context['day'] = day
        return day

    def get_context(self):
        self.year = self.get_year() # use ths func
        self.month = self.get_month()
        self.day = self.get_day()
        self.context['form'] = DiaryUpdateForm(self.request.POST or None)
        return self.context


    def get_date_data(self, **kwargs):
        kwargs.setdefault('today', timezone.now)
        
    def get(self, request, *args, **kwargs):
        print(self.context)
        return render(request, self.template_name, self.get_context())
   
    def post(self, request, *args, **kwargs):
        messages.success(request, 'You submitted a form!')
        print(self.context)
        return render(request, self.template_name, self.get_context())



class NewProfile(View):
    template_name = 'profiles/profile2.html'
    context = {}

    def get_context(self, **kwargs):
        
        return self.kwargs

    def get(self, request, *args, **kwargs):
        print(self.__dict__)
        return render(request, self.template_name, self.get_context())
   
    def post(self, request, *args, **kwargs):
        print(self.__dict__)
        return render(request, self.template_name, self.get_context())
 




