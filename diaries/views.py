import datetime

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
from django.views.generic.base import ContextMixin
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from food.forms import FOOD_SORT_CHOICES, FoodFilterForm
from food.models import Food
from meals.models import Meal, MealItem

from .forms import AddRecentToDiaryFormSet, AddToDiaryFormSet, DiaryUpdateForm
from .mixins import DiaryDateMixin, DiaryMealMixin, FoodFilterMixin
from .models import Diary



class DiaryDayListView(LoginRequiredMixin, DiaryDateMixin, ListView):
    """
    Displays a list of food objects by date, associated quantities, calculated calorie and macronutrient values for a given day.
    Defaults to displaying data today
    TODO: Use django window function instead calling total multiple times.
    """

    template_name = 'diaries/diary_day_list.html'
    
    def get_queryset(self):
        self.get_diary_date() # from DiaryDateMixin
        return Diary.objects.filter(user=self.request.user, date=self.date).summary().order_by('datetime_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().total()
        context['target'] = self.request.user.profile
        context['remaining'] = self.get_queryset().remaining(user=self.request.user)
        context['total_meal_1'] = self.get_queryset().filter(meal=1).total()
        context['total_meal_2'] = self.get_queryset().filter(meal=2).total()
        context['total_meal_3'] = self.get_queryset().filter(meal=3).total()
        context['total_meal_4'] = self.get_queryset().filter(meal=4).total()
        context['total_meal_5'] = self.get_queryset().filter(meal=5).total()
        context['total_meal_6'] = self.get_queryset().filter(meal=6).total()
        return context

    def post(self, request, *args, **kwargs):
        self.get_diary_date()
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


class DiaryMealDetailView(LoginRequiredMixin, DiaryDateMixin, DiaryMealMixin, ListView):
    """
    Displays a detail view of a diary meal and associated food, quantities and calories/macronutrients.
    """
    template_name = 'diaries/diary_meal_list.html'
    def get_queryset(self):
        self.get_diary_date()
        return Diary.objects.filter(user=self.request.user, date=self.date, meal=self.meal).summary()

    def get_context_data_data(self, **kwargs):
        context = super().get_context_data_data(**kwargs)
        context['total'] = self.get_queryset().total()
        context['total_meal'] = self.get_queryset().filter(meal=self.meal).total()
        return context


def diary_meal_update_view(request, year, month, day, meal):
    try:
        date = datetime.date(year, month, day)
    except ValueError as e:
        raise Http404(e)
    if not meal in range(1,7):
        raise Http404('Invalid meal')

    template_name = 'diaries/diary_meal_update.html'
    context = {}

    queryset = Diary.objects.filter(user=request.user, date=date, meal=meal).summary()

    context['meal_name'] = [x[1] for x in Diary.Meal.choices if x[0] == meal][0]
    context['object_list'] = queryset
    return render(request, template_name, context)



class DiaryAddMultipleFoodView(DiaryDateMixin, DiaryMealMixin, FoodFilterMixin, TemplateView):
    """
    View for the user to add multiple food to their diary via a formset. 
    Using template view as the main view class as it provides a get method.
    # TODO clean pagination - looks a bit messy, will be better way to do this.
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
        print('1',self.__dict__)
        context = self.get_context_data(**kwargs)
        formset = AddToDiaryFormSet(self.request.POST, initial=context.get('queryset'))
        print('2', self.__dict__)
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




class DiaryMealCopyPreviousDay(DiaryDateMixin, DiaryMealMixin, View):
    template_name = 'diaries/diary_copy_previous_day.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object_list = Diary.objects.filter(user=self.request.user, date=self.previous_day, meal=self.diary_meal).summary()
        context['object_list'] = self.object_list
        return context

    def get(self, request, *args, **kwargs):
        print('get', self.__dict__)
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        print(self.__dict__)
        context = self.get_context_data(**kwargs)
        print(self.__dict__)
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


@login_required
def diary_copy_meal_from_previous_day_view(request, year, month, day, meal):
    
    try:
        date = datetime.date(year, month, day)
        previous_day = date - datetime.timedelta(days=1)
    except ValueError as e:
        raise Http404(e)

    if meal in range(1,7):
        meal_name = [x[1] for x in Diary.Meal.choices if x[0] == meal][0]
    else:    
        raise Http404('Invalid meal')

    template_name = 'diaries/diary_copy_previous_day.html'
    context = {}
    
    # meal_list = MealItem.objects.filter(meal_id='e3a38240-ea6a-40b3-a6b8-d2b4460503a6')
    # for obj in meal_list:
    #     print(obj.food_id)
    #     print(obj.quantity)

    object_list = Diary.objects.filter(user=request.user, date=previous_day, meal=meal).summary()
    if request.method == 'POST':
        if object_list:
            for obj in object_list:
                Diary.objects.create(
                    user=request.user,
                    date=date,
                    meal=meal,
                    food=obj.food,
                    quantity=obj.quantity,
                )
            messages.success(request, f'Copied {len(object_list)} food from {meal_name}, {previous_day}')
            return redirect('diaries:day', date.year, date.month, date.day)
    context['date'] = date
    context['previous_day'] = previous_day
    context['meal'] = meal
    context['meal_name'] = meal_name
    context['object_list'] = object_list
    context['total'] = object_list.total()
    return render(request, template_name, context)


@login_required
def diary_copy_all_meals_from_previous_day_view(request, year, month, day):
    template_name = ''
    context = {}
    return render(request, template_name, context)


@login_required
def diary_update_view(request, pk):
    """
    Diary detail and update vi
    
    w, allows users to view the macronutrient content of the food 
    they've added to their dia
    
    y and edit the quantity.
    Redirect users that don't belong here.
    """

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



class DiaryUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Diary
    form_class = DiaryUpdateForm
    success_message = 'Updated %(food_name)s'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, food_name=self.object.food)

    def get_success_url(self):
        obj = self.get_object()
        return reverse('diaries:day', kwargs={'year': obj.date.year, 'month': obj.date.month, 'day': obj.date.day})



class DiaryDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
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






""" Adding saved meals to diary """

class DiaryAddMealView(DiaryDateMixin, DiaryMealMixin, TemplateView):
    # TODO: Use a list view to provide pagination
    
    template_name = 'diaries/diary_add_meal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Meal.objects.filter(user=self.request.user)
        return context




""" In progress - to replace the below FBV """
class DiaryAddMealConfirmView(DiaryDateMixin, DiaryMealMixin, TemplateView):
    template_name = 'diaries/browse_saved_meals.html'

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
""" In progress - to replace the below FBV """


def diary_add_meal_confirm_view(request, year, month, day, meal, saved_meal):
    """ View to allow user to confirm the saved meal addition to diary meal. """
    try:
        date = datetime.date(year, month, day)
    except ValueError as e:
        raise Http404(e)
    if meal in range(1,7):
        meal_name = [x[1] for x in Diary.Meal.choices if x[0] == meal][0]
    else:    
        raise Http404('Invalid meal')
    
    saved_meal_obj = get_object_or_404(Meal, id=saved_meal)
    template_name = 'diaries/diary_add_meal_confirm.html'
    context = {}
    meal_item_list = MealItem.objects.filter(meal_id=saved_meal_obj)
    
    if request.method == 'POST':
        if meal_item_list:
            for food_item in meal_item_list:
                Diary.objects.create(
                    user=request.user,
                    date=date,
                    meal=meal,
                    food=food_item.food,
                    quantity=food_item.quantity
                )
            messages.success(request, f'Added {len(meal_item_list)} items from {saved_meal_obj} to {meal_name}')
            return redirect('diaries:day', date.year, date.month, date.day)
    return render(request, template_name, context)






""" Unused """

""" Replaced by CBV """
def diary_add_multiple_food_view(request, year, month, day, meal):
    """ Displays a list/formset view for the user to add food to their selected diary meal in bulk. """

    # Validating date and meal url parameters
    try:
        date = datetime.date(year, month, day)
    except ValueError as e:
        raise Http404(e)

    if meal not in range(1,7): # changed.
        raise Http404('Invalid meal')
    meal_name = [x[1] for x in Diary.Meal.choices if x[0] == meal][0]
    
    template_name = 'diaries/diary_add_food_multiple.html'
    context = {}
    queryset = Food.objects.summary().values()

    # Search / filter component
    q = request.GET.get('q')
    brand = request.GET.get('brand')
    category = request.GET.get('category')
    sort = request.GET.get('sort')
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
    
    if request.method == 'POST':
        formset = AddToDiaryFormSet(request.POST, initial=queryset)
        if formset.is_valid():
            count = 0
            for form in formset:
                attrs = form.cleaned_data
                if attrs['quantity']:
                    attrs['food_id'] = attrs.pop('id')
                    attrs['user'] = request.user
                    attrs['date'] = date
                    attrs['meal'] = meal
                    count += 1
                    Diary.objects.create(**attrs)

            if 'save' in request.POST:
                messages.success(request, f'Added {count} food to {meal_name}, {date}')
                return redirect('diaries:day', date.year, date.month, date.day)

            elif 'another' in request.POST:
                messages.success(request, f'Added {count } food to {meal_name}, {date}. You can continue adding food below')
                return redirect('diaries:create', date.year, date.month, date.day, meal)

    else:
        formset = AddToDiaryFormSet(initial=queryset)

    context['management_data'] = formset

    paginator = Paginator(formset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['date'] = date
    context['meal'] = meal
    context['meal_name'] = meal_name
    context['meal_list'] = Diary.objects.filter(user=request.user, date=date, meal=meal).summary()
    context['formset'] = page_obj
    context['form'] = FoodFilterForm(request.GET)
    return render(request, template_name, context)

def diary_add_meal_view(request, year, month, day, meal):
    try:
        date = datetime.date(year, month, day)
    except ValueError as e:
        raise Http404(e)
    if meal in range(1,7):
        meal_name = [x[1] for x in Diary.Meal.choices if x[0] == meal][0]
    else:    
        raise Http404('Invalid meal')

    template_name = 'diaries/diary_add_meal.html'
    context = {}

    context['object_list'] = Meal.objects.filter(user=request.user)
    context['date'] = date
    context['meal'] = meal
    context['meal_name'] = meal

