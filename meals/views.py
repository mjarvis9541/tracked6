from django.forms.forms import Form
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from meals.models import Meal, MealItem
from django.views.generic import CreateView, FormView, ListView, View, TemplateView
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from food.models import Food
from food.mixins import FoodFilterMixin
from food.forms import FoodFilterForm
from diaries.forms import AddToDiaryFormSet, BaseDiaryFormset
from .forms import AddToMealFormSet, MealItemForm, MealCreateForm, AddToMealForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class MealListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)


class MealCreateView(LoginRequiredMixin, CreateView):
    """ Step 1: Create a meal (name, description). """

    template_name = 'meals/meal_create.html'
    model = Meal
    form_class = MealCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('meals:meal_add_1', kwargs={'meal_id': self.object.id})


class MealItemCreateStep1View(LoginRequiredMixin, UserPassesTestMixin, FoodFilterMixin, ListView):
    """ Step 2: Find food to add to the meal. """

    model = Food
    template_name = 'meals/meal_add_1.html'
    paginate_by = 20

    def test_func(self):
        meal = get_object_or_404(Meal, id=self.kwargs.get('meal_id'))
        return meal.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FoodFilterForm(self.request.GET)
        context['meal'] = get_object_or_404(Meal, id=self.kwargs.get('meal_id'))
        return context


class MealItemCreateStep2View(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """ Step 3: Display food details and render form to enable user to add food to the meal. """

    template_name = 'meals/meal_add_2.html'

    def test_func(self):
        meal = get_object_or_404(Meal, id=self.kwargs.get('meal_id'))
        return meal.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['food'] = get_object_or_404(Food, id=self.kwargs.get('food_id'))
        context['meal'] = get_object_or_404(Meal, id=self.kwargs.get('meal_id'))
        context['form'] = AddToMealForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form = AddToMealForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.meal = context.get('meal')
            instance.food = context.get('food')
            instance.save()
            return redirect(instance.get_absolute_url())
        return render(request, self.template_name, context)


class MealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Delete a meal and return user to meal list view. """

    model = Meal
    success_url = reverse_lazy('meals:list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'Deleted {self.get_object().name}')
        return super().delete(request, *args, **kwargs)


class MealItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Delete a food from meal and return user to the meal detail view of the deleted food. """

    model = MealItem

    def test_func(self):
        obj = self.get_object()
        return obj.meal.user == self.request.user

    def get_success_url(self):
        obj = self.get_object()
        return reverse('meals:detail', kwargs={'pk': obj.meal.id})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'Deleted {obj.food.name} from {obj.meal.name}')
        return super().delete(request, *args, **kwargs)


class MealItemListView(ListView):
    def get_queryset(self):
        return MealItem.objects.filter(meal=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(Meal, id=self.kwargs.get('pk'))
        return context


class MealDetailView(DetailView):
    model = Meal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mealitem_set'] = self.object.mealitem_set.all()
        return context


class MealItemDetailView(DetailView):
    model = MealItem
    template_name = 'meals/meal_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mealitem_set'] = self.object.mealitem_set.all()
        return context
