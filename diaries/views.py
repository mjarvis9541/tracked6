from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Case, F, Q, Value, When
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import (HttpResponseRedirect, get_list_or_404,
                              get_object_or_404, redirect, render)
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DayArchiveView, DeleteView,
                                  FormView, ListView, TemplateView,
                                  TodayArchiveView, UpdateView, View,
                                  WeekArchiveView)
from food.models import Food
from meals.models import Meal, MealItem

from .forms import AddRecentToDiaryFormSet, AddToDiaryFormSet, DiaryUpdateForm
from .mixins import DiaryDateMixin, DiaryMealMixin, FoodFilterMixin
from .models import Diary

User = get_user_model()


""" Diary list views """


class DiaryDayListView(LoginRequiredMixin, DiaryDateMixin, TemplateView):
    """
    * Displays a list of food objects a user has added to their food diary on a given day.
    * The given day is either passed into the url, or by default set to the current day.
    * Data shown is the food, quantity, calculated calories and macronutrients.
    * Renders the users daily total of calculated calorie and macronutrients from food and associated quantities added.
    * Renders the users daily target from their profile calorie and macronutrients targets.
    * Renders the remaining values of the users daily total minus the users daily target.
    """

    template_name = 'diaries/diary_day_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ = self.request.user
        object_list = Diary.objects.filter(user=user_, date=self.date).summary().order_by('datetime_created')
        context['object_list'] = object_list 
        context['total'] = object_list.total()
        context['total_meal_1'] = object_list.filter(meal=1).total()
        context['total_meal_2'] = object_list.filter(meal=2).total()
        context['total_meal_3'] = object_list.filter(meal=3).total()
        context['total_meal_4'] = object_list.filter(meal=4).total()
        context['total_meal_5'] = object_list.filter(meal=5).total()
        context['total_meal_6'] = object_list.filter(meal=6).total()
        context['target'] = user_.profile
        context['remaining'] = object_list.remaining(user=user_)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs) 
        obj_list = request.POST.getlist('to_delete')
        if obj_list: 
            delete_list = Diary.objects.filter(id__in=obj_list)
            count = len(delete_list)
            for obj in delete_list:
                if obj.user != request.user:
                    return HttpResponseForbidden('You are not authorized to delete this user\'s diary entries')
            request.session['delete_list'] = obj_list
            messages.success(request, f'Selected {count} food to delete')
            return redirect('diaries:delete_list') 
        else:
            messages.error(request, 'You have not selected any food to delete')
        return self.render_to_response(context)


class DiaryMealListView(LoginRequiredMixin, DiaryDateMixin, DiaryMealMixin, TemplateView):
    """
    Gives a breakdown of food for a given meal in a singular view.
    * Helps mobile users view full calorie and macronutrient content of food as the page is to be displayed with more detail in mobile view. 
    """
    
    template_name = 'diaries/diary_meal_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Diary.objects.filter(user=self.request.user, date=self.date).summary() 
        context['total'] = context['object_list'].total() 
        return context


""" Diary create views """


class DiaryAddMultipleFoodView(LoginRequiredMixin, DiaryDateMixin, DiaryMealMixin, FoodFilterMixin, TemplateView):
    """
    Allows the user to add multiple food items to their food diary via formset.
    Renders the formset with food name and details and a quantity input field.
    """
    
    template_name = 'diaries/diary_add_food_multiple.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['queryset'], 20) # FoodFilterMixin
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['formset'] = AddToDiaryFormSet(data=self.request.POST or None, initial=page_obj)
        return context
  
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['formset'].is_valid():
            count = 0
            for form in context['formset'].cleaned_data:
                if form['quantity']:
                    form['food_id'] = form.pop('id')
                    form['user'] = request.user
                    form['date'] = self.date
                    form['meal'] = self.diary_meal
                    count += 1
                    Diary.objects.create(**form)

            if 'save' in request.POST:
                messages.success(request, f'Added {count} food to {self.diary_meal_name}, {self.date}')
                return redirect('diaries:day', self.date.year, self.date.month, self.date.day)

            elif 'another' in request.POST:
                messages.success(request, f'Added {count} food to {self.diary_meal_name}, {self.date}. You can continue adding food below')
                return redirect('diaries:create', self.date.year, self.date.month, self.date.day, self.diary_meal)
        
        return self.render_to_response(context)


class DiaryCopyMealPreviousDay(LoginRequiredMixin, DiaryDateMixin, DiaryMealMixin, TemplateView):
    """ 
    Allows the user to copy all food and quantities from the specified 
    diary meal on a previous day to the same diary meal on the diary 
    day they are currently viewing.
    """
    
    template_name = 'diaries/diary_copy_previous_day.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Diary.objects.filter(user=self.request.user, date=self.previous_day, meal=self.diary_meal).summary()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = context['object_list']
        if object_list:
            count = len(object_list)
            for obj in object_list:
                Diary.objects.create(
                    user=self.request.user,
                    date=self.date,
                    meal=self.diary_meal,
                    food=obj.food,
                    quantity=obj.quantity,
                )
            messages.success(request, f'Copied {count} food from {self.diary_meal_name}, {self.previous_day}')
            return redirect('diaries:day', self.date.year, self.date.month, self.date.day)
        return self.render_to_response(context)


class DiaryCopyAllMealPreviousDay(LoginRequiredMixin, DiaryDateMixin, TemplateView):
    """
    Allows the user to copy all food and associated quantities from the previous diary day.
    TODO: Copies food even if the user has the same amount of food for 
    a meal already - need a way to handle this as unlikely user will want to add duplicates 
    """
    template_name = 'diaries/diary_copy_previous_day.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Diary.objects.filter(user=self.request.user, date=self.previous_day).summary()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = context['object_list']
        if object_list:
            count = len(object_list)
            for obj in object_list:
                Diary.objects.create(
                    user=self.request.user,
                    date=self.date,
                    meal=obj.meal,
                    food=obj.food,
                    quantity=obj.quantity,
                )
            messages.success(request, f'Copied {count} food from {self.previous_day}')
            return redirect('diaries:day', self.date.year, self.date.month, self.date.day)
        return self.render_to_response(context)


class DiaryAddMealView(LoginRequiredMixin, DiaryDateMixin, DiaryMealMixin, TemplateView):
    """
    Displays a list of users saved meals to select from and add to the food diary. 
    """

    template_name = 'diaries/diary_add_meal_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Meal.objects.filter(user=self.request.user)
        return context


class DiaryAddMealConfirmView(LoginRequiredMixin, DiaryDateMixin, DiaryMealMixin, TemplateView):
    """
    Allows the user to confirm addition of their chosen saved meal to the diary meal specified in URL parameters.
    """

    template_name = 'diaries/diary_add_meal_confirm.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['saved_meal_obj'] = get_object_or_404(Meal, id=self.kwargs.get('saved_meal'))
        context['object_list'] = MealItem.objects.filter(meal_id=context['saved_meal_obj'])
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        saved_meal_obj = context['saved_meal_obj']
        meal_item_list = context['object_list']
        if meal_item_list:
            count = len(meal_item_list)
            for food_item in meal_item_list:
                Diary.objects.create(
                    user=request.user,
                    date=self.date,
                    meal=self.diary_meal,
                    food=food_item.food,
                    quantity=food_item.quantity
                )
            messages.success(request, f'Added {count} items from saved meal {saved_meal_obj} to {self.diary_meal_name}, {self.date}')
            return redirect('diaries:day', self.date.year, self.date.month, self.date.day)
        return self.render_to_response(context)


""" Diary update views """


class DiaryUpdateView(LoginRequiredMixin, DiaryDateMixin, TemplateView):
    template_name = 'diaries/diary_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Diary.objects.filter(id=self.kwargs.get('pk')).summary().first()
        context['form'] = DiaryUpdateForm(self.request.POST or None, instance=context['object'])
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_ = context['object']
        date = context['object'].date
        if context['form'].is_valid():
            context['form'].save()
            
            if 'save' in request.POST:
                messages.success(request, f'Updated {object_.food_name}, {object_.get_meal_display()}')
                return redirect('diaries:day', date.year, date.month, date.day)
            
            elif 'another' in request.POST:
                messages.success(request, f'{object_.get_meal_display()} - {object_.food_name} has been updated. You can add more food below')
                return redirect('diaries:create', date.year, date.month, date.day, object_.meal)
        
        return self.render_to_response(context)


""" Diary delete views """


class DiaryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows the user to confirm deletion of single diary food item.
    """
    model = Diary

    def get_context_data_data(self, **kwargs):
        context =  super().get_context_data_data(**kwargs)
        context['date'] = self.get_object().date
        return context

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.warning(self.request, f'{obj.food.name} was deleted')
        return super().delete(self.request, *args, **kwargs)

    def get_success_url(self):
        obj = self.get_object()
        return reverse('diaries:day', kwargs={'year': obj.date.year, 'month': obj.date.month, 'day': obj.date.day})


class DiaryDeleteMultipleView(LoginRequiredMixin, TemplateView):
    """
    Allows the user to confirm deletion of multiple diary food items selected via checkboxes (sessions) from DiaryDayListView.
    """
    template_name = 'diaries/diary_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_list = self.request.session.get('delete_list')
        if delete_list:
            context['object_list'] = Diary.objects.filter(id__in=delete_list)
            context['date'] = context['object_list'].first().date
            context['meal_name'] = context['object_list'].first().get_meal_display()
        else:
            context['date'] = timezone.now()
            context['meal_name'] = None
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = context['object_list']
        count = len(object_list)
        date = context['date']
        meal = context['meal_name']
        if object_list:
            object_list.delete()
            request.session.pop('delete_list')
            messages.success(request, f'Deleted {count} food from {meal}, {date}')
            return redirect('diaries:day', date.year, date.month, date.day) 
        return self.render_to_response(context)
    

""" Diary list views - to view other user diaries """


class DiaryUserDayListView(LoginRequiredMixin, DiaryDateMixin, TemplateView):
    """
    View to display other user's food diaries.
    TODO: We need to create another template and remove visuals on 
    creating, updating and delete food from diary.
    """

    template_name = 'diaries/diary_list_alt_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ = get_object_or_404(User, username=self.kwargs.get('username'))
        object_list = Diary.objects.filter(user__username=self.kwargs.get('username'), date=self.date).summary().order_by('datetime_created')
        context['object_list'] = object_list 
        context['total'] = object_list.total()
        context['total_meal_1'] = object_list.filter(meal=1).total()
        context['total_meal_2'] = object_list.filter(meal=2).total()
        context['total_meal_3'] = object_list.filter(meal=3).total()
        context['total_meal_4'] = object_list.filter(meal=4).total()
        context['total_meal_5'] = object_list.filter(meal=5).total()
        context['total_meal_6'] = object_list.filter(meal=6).total()
        context['target'] = user_.profile
        context['remaining'] = object_list.remaining(user=user_)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs) 
        obj_list = request.POST.getlist('to_delete')
        if obj_list: 
            delete_list = Diary.objects.filter(id__in=obj_list)
            count = len(delete_list)
            for obj in delete_list:
                if obj.user != request.user:
                    return HttpResponseForbidden('You are not authorized to delete this user\'s diary entries')
            request.session['delete_list'] = obj_list
            messages.success(request, f'Selected {count} food to delete')
            return redirect('diaries:delete_list') 
        else:
            messages.error(request, 'You have not selected any food to delete')
        return self.render_to_response(context)