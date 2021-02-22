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
from food.mixins import FoodFilterMixin
from food.models import Food

from .forms import AddRecentToDiaryFormSet, AddToDiaryFormSet, DiaryUpdateForm
from .mixins import DateMixin, MealMixin
from .models import Diary


class DiaryDayListView(LoginRequiredMixin, DateMixin, ListView):
    """ Displays all the food a user has consumed and tracked on a given day. """
    template_name = 'diaries/diary_list.html'

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user, date=self.date).summary().order_by('datetime_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target'] = self.request.user.profile
        context['remaining'] = self.get_queryset().remaining(user=self.request.user)
        context['total'] = self.get_queryset().total()
        context['total_meal_1'] = self.get_queryset().filter(meal=1).total()
        context['total_meal_2'] = self.get_queryset().filter(meal=2).total()
        context['total_meal_3'] = self.get_queryset().filter(meal=3).total()
        context['total_meal_4'] = self.get_queryset().filter(meal=4).total()
        context['total_meal_5'] = self.get_queryset().filter(meal=5).total()
        context['total_meal_6'] = self.get_queryset().filter(meal=6).total()
        return context


    def post(self, request, *args, **kwargs):
        obj_list = request.POST.getlist('to_delete')
        if obj_list: 
            delete_list = Diary.objects.filter(id__in=obj_list)
            # msg_list = []
            for obj in delete_list:
                if obj.user != request.user:
                    return HttpResponseForbidden('You are not authorized to delete this user\'s diary entry')
            request.session['delete_list'] = obj_list
            # delete_list.delete()
            # messages.success(request, f'Food deleted: {msg_list}')
            # messages.success(request, f'Food deleted')
            return redirect('diaries:delete_list') 
        else:
            messages.error(request, 'You have not selected any food to delete')
        return redirect('diaries:day', self.date.year, self.date.month, self.date.day) 




class DiaryMealListView(LoginRequiredMixin, DateMixin, MealMixin, ListView):
    template_name = 'diaries/diary_meal_list.html'

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user, date=self.date, meal=self.meal).summary()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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




def add_to_diary_view(request, year, month, day, meal):
    """ Displays a list/formset view for the user to add food to their selected diary meal in bulk. """

    try:
        date = datetime.date(year, month, day)
    except ValueError as e:
        raise Http404(e)
    if not meal in range(1,7):
        raise Http404('Invalid meal')

    template_name = 'diaries/diary_add_food.html'
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
            pass
    if category:
        try:
            queryset = queryset.filter(category=category)
        except Exception:
            pass
    if sort and any(sort in x for x in FOOD_SORT_CHOICES):
        queryset = queryset.order_by(sort)
    
    # Adding the food via formset
    if request.method == 'POST':
        formset = AddToDiaryFormSet(request.POST, initial=queryset)
        if formset.is_valid():
            # data = []
            for form in formset:
                attrs = form.cleaned_data
                if attrs['quantity']:
                    attrs['food_id'] = attrs.pop('id')
                    attrs['user'] = request.user
                    attrs['date'] = date
                    attrs['meal'] = meal
                    Diary.objects.create(**attrs)
                    # data.append(attrs)

            if 'save' in request.POST:
                messages.success(request, 'Food added')
                return redirect('diaries:day', date.year, date.month, date.day)

            elif 'another' in request.POST:
                messages.success(request, 'Food added. You can continue adding food below')
                return redirect('diaries:create', date.year, date.month, date.day, meal)

    else:
        formset = AddToDiaryFormSet(initial=queryset)

    context['management_data'] = formset

    paginator = Paginator(formset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['date'] = date
    context['meal'] = meal
    context['meal_name'] = [x[1] for x in Diary.Meal.choices if x[0] == meal][0]
    context['meal_list'] = Diary.objects.filter(user=request.user, date=date, meal=meal).summary()
    context['formset'] = page_obj
    context['form'] = FoodFilterForm(request.GET)
    return render(request, template_name, context)


@login_required
def copy_meal_from_previous_day_view(request, year, month, day, meal):
    
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
def copy_all_meals_from_yesterday_view(request, year, month, day):
    template_name = ''
    context = {}
    return render(request, template_name, context)


@login_required
def diary_update_view(request, pk):
    """
    Diary detail and update view, allows users to view the macronutrient content of the food 
    they've added to their diary and edit the quantity.
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
def diary_delete_list_view(request):
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

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
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






