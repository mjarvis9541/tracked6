from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Case, F, Q, Value, When
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
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
        object_list = Diary.objects.filter(user=user_, date=self.date).summary()
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
        self.get_diary_date() # method of DiaryDateMixin
        # TODO: self.get_context_data(**kwargs) to replace above once tested.
        obj_list = request.POST.getlist('to_delete')
        if obj_list: 
            delete_list = Diary.objects.filter(id__in=obj_list)
            for obj in delete_list:
                if obj.user != request.user:
                    return HttpResponseForbidden('You are not authorized to delete this user\'s diary entries')
            request.session['delete_list'] = obj_list
            return redirect('diaries:delete_list') 
        else:
            messages.error(request, 'You have not selected any food to delete')
        return redirect('diaries:day', self.date.year, self.date.month, self.date.day) 


class DiaryMealListView(LoginRequiredMixin, DiaryDateMixin, DiaryMealMixin, TemplateView):
    """
    Gives a breakdown of food for a given meal in a singular view.
    * Helps mobile users view full calorie and macronutrient content of food as the page is to be displayed with more detail in mobile view. 
    """
    
    template_name = 'diaries/diary_meal_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = Diary.objects.filter(user=self.request.user, date=self.date).summary()
        context['object_list'] = object_list 
        context['total'] = object_list.total() 
        return context


class DiaryAddMultipleFoodView(LoginRequiredMixin, DiaryDateMixin, DiaryMealMixin, FoodFilterMixin, TemplateView):
    """
    Allows the user to add multiple food items to their food diary via formset.
    Renders the formset with food name and details and a quantity input field.
    FIXME: Work on formset pagination code as view currently looks quite convoluted.
    """

    template_name = 'diaries/diary_add_food_multiple.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formset = AddToDiaryFormSet(initial=context.get('queryset'))

        context['management_data'] = formset
        paginator = Paginator(formset, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['formset'] = page_obj

        return context
   
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        formset = AddToDiaryFormSet(self.request.POST, initial=context.get('queryset'))
        if formset.is_valid():
            count = 0
            for form in formset.cleaned_data:
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
        
        context['management_data'] = formset
        paginator = Paginator(formset, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['formset'] = page_obj

        return render(request, self.template_name, context)


class DiaryCopyMealPreviousDay(LoginRequiredMixin, DiaryDateMixin, DiaryMealMixin, TemplateView):
    """ 
    Allows the user to copy all food and quantities from the specified 
    diary meal on a previous day to the same diary meal on the diary 
    day they are currently viewing.
    """
    
    template_name = 'diaries/diary_copy_previous_day.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object_list = Diary.objects.filter(user=self.request.user, date=self.previous_day, meal=self.diary_meal).summary()
        context['object_list'] = self.object_list
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.object_list:
            for obj in self.object_list:
                Diary.objects.create(
                    user=self.request.user,
                    date=self.date,
                    meal=self.diary_meal,
                    food=obj.food,
                    quantity=obj.quantity,
                )
            messages.success(request, f'Copied {len(self.object_list)} food from {self.diary_meal_name}, {self.previous_day}')
            return redirect('diaries:day', self.date.year, self.date.month, self.date.day)
        return render(request, self.template_name, context)


class DiaryCopyAllMealPreviousDay(LoginRequiredMixin, DiaryDateMixin, DiaryMealMixin, TemplateView):
    """
    Allows the user to copy all food and associated quantities from the previous diary day.
    TODO: Complete the view.
    """
    pass


class DiaryAddMealView(LoginRequiredMixin, DiaryDateMixin, DiaryMealMixin, TemplateView):
    """
    Shows the user a list of their saved meals to select and add to the diary meal specified in URL parameters. 
    """

    template_name = 'diaries/diary_add_meal.html'

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
        saved_meal_obj = get_object_or_404(Meal, id=self.kwargs.get('saved_meal'))
        meal_item_list = MealItem.objects.filter(meal_id=saved_meal_obj)
        context['object_list'] = meal_item_list
        return context


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        saved_meal_obj = get_object_or_404(Meal, id=self.kwargs.get('saved_meal'))
        meal_item_list = MealItem.objects.filter(meal_id=saved_meal_obj)
        context['object_list'] = meal_item_list
        if meal_item_list:
            for food_item in meal_item_list:
                Diary.objects.create(
                    user=request.user,
                    date=self.date,
                    meal=self.diary_meal,
                    food=food_item.food,
                    quantity=food_item.quantity
                )
            messages.success(request, f'Added {len(meal_item_list)} items from saved meal {saved_meal_obj} to {self.diary_meal_name}, {self.date}')
            return redirect('diaries:day', self.date.year, self.date.month, self.date.day)
        return render(request, self.template_name, context)


class DiaryUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DiaryDateMixin, UpdateView):
    model = Diary
    form_class = DiaryUpdateForm
    template_name = 'diaries/diary_update.html'
    success_message = 'Updated %(food_name)s'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, food_name=self.object.food)

    def get_success_url(self):
        obj = self.get_object()
        return reverse('diaries:day', kwargs={'year': obj.date.year, 'month': obj.date.month, 'day': obj.date.day})


@login_required
def diary_update_view(request, pk):
    template_name = 'diaries/diary_update.html'
    context = {}
    obj = Diary.objects.filter(id=pk).summary().first()

    if obj.user != request.user:
        return HttpResponseForbidden()
    date = obj.date

    if request.method == 'POST':
        form = DiaryUpdateForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            if 'save' in request.POST:
                messages.success(request, f'Updated {obj.food_name}, {obj.get_meal_display()}')
                return redirect('diaries:day', date.year, date.month, obj.date.day)

            elif 'another' in request.POST:
                messages.success(request, f'{obj.get_meal_display()} - {obj.food_name} has been updated. You can add more food below')
                return redirect('diaries:create', date.year, date.month, date.day, obj.meal)
    else:
        form = DiaryUpdateForm(instance=obj)

    context['date'] = obj.date
    context['object'] = obj
    context['form'] = form
    return render(request, template_name, context)


@login_required
def diary_delete_multiple_food_view(request):
    """
    Allows the user to confirm deletion of multiple diary food items selected via checkboxes (sessions) from DiaryDayListView.
    """
    template_name = 'diaries/diary_confirm_delete.html'
    context = {}

    obj_list = request.session.get('delete_list')
    if obj_list: 
        obj_list = Diary.objects.filter(id__in=obj_list)
        date = obj_list.first().date
        meal = obj_list.first().get_meal_display()
    else:
        date = timezone.now()
        meal = None
    
    if request.method == 'POST':
        if obj_list: 
            Diary.objects.filter(id__in=obj_list).delete()
            request.session.pop('delete_list')
            messages.success(request, f'Deleted {len(obj_list)} food from {meal}, {date}')
            return redirect('diaries:day', date.year, date.month, date.day) 
    
    context['meal_name'] = meal
    context['date'] = date
    context['object_list'] = obj_list
    return render(request, template_name, context)


class DiaryDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
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

