from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, ListView, TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from food.forms import FoodFilterForm
from food.mixins import FoodFilterMixin
from food.models import Food

from .forms import AddToMealForm, MealCreateForm
from .models import Meal, MealItem


class MealListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user).summary().order_by('name')


class MealCreateView(LoginRequiredMixin, CreateView):
    """ Step 1: Create a meal (name, description). """

    template_name = 'meals/meal_create.html'
    model = Meal
    form_class = MealCreateForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('meals:meal_add_1', kwargs={'meal_id': self.object.pk})


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
        context['form'] = AddToMealForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['form'].is_valid():
            instance = context['form'].save(commit=False)
            instance.meal = context.get('meal')
            instance.food = context.get('food')
            instance.save()
            return redirect(instance.get_absolute_url())
        return self.render_to_response(context)



class MealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Delete a meal and return user to meal list view. """

    model = Meal
    success_url = reverse_lazy('meals:list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'Deleted Meal {obj.name}')
        return super().delete(request, *args, **kwargs)


class MealItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Delete a food from meal and return user to the meal detail view of the deleted food. """

    model = MealItem

    def test_func(self):
        obj = self.get_object()
        return obj.meal.user == self.request.user

    def get_success_url(self):
        obj = self.get_object()
        return reverse('meals:item_list', kwargs={'pk': obj.meal.pk})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'Deleted {obj.food.name} from {obj.meal.name}')
        return super().delete(request, *args, **kwargs)


class MealItemListView(ListView):
    def get_queryset(self):
        return MealItem.objects.filter(meal=self.kwargs.get('pk')).summary()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(Meal, id=self.kwargs.get('pk'))
        context['total'] = self.get_queryset().total()
        return context



class MealItemDetailView(DetailView):
    model = MealItem
    template_name = 'meals/meal_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mealitem_set'] = self.object.mealitem_set.all()
        return context
