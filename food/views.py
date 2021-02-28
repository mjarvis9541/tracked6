from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)
from django.views.generic.detail import SingleObjectMixin

from .forms import (
    BrandCreateForm,
    BrandFilterForm,
    FoodCreateServingForm,
    FoodDetailToDiaryForm,
    FoodFilterForm,
    FoodToDiaryForm,
    FoodToMealForm,
)
from .mixins import BrandFilterMixin, FoodFilterMixin
from .models import Brand, Category, Food
from .utils import data_to_serving, serving_to_data


class BrandListView(BrandFilterMixin, ListView):
    model = Brand
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BrandFilterForm(self.request.GET)
        return context


class BrandCreateView(LoginRequiredMixin, CreateView):
    model = Brand
    form_class = BrandCreateForm

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.user_updated = self.request.user
        return super().form_valid(form)


class BrandDetailView(DetailView):
    model = Brand


class BrandUpdateView(LoginRequiredMixin, UpdateView):
    model = Brand
    form_class = BrandCreateForm

    def form_valid(self, form):
        form.instance.user_updated = self.request.user
        return super().form_valid(form)


class BrandDeleteView(LoginRequiredMixin, DeleteView):
    model = Brand
    success_url = reverse_lazy('food:brand_list')


class CategoryListView(ListView):
    model = Category
    paginate_by = 25


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ('name', 'description')

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.user_updated = self.request.user
        return super().form_valid(form)


class CategoryDetailView(DetailView):
    model = Category


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ('name', 'description')

    def form_valid(self, form):
        form.instance.user_updated = self.request.user
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('food:category_list')


class FoodListView(FoodFilterMixin, ListView):
    ordering = ('name', 'brand')
    paginate_by = 20
    queryset = Food.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FoodFilterForm(self.request.GET)
        context['latest_food'] = Food.objects.all().order_by('-datetime_created')[:10]
        return context


class FoodCreateView(LoginRequiredMixin, CreateView):
    """
    Food create view with one 'serving' form field to combine and replace
    the two model fields 'data_value' and 'data_measurement'
    """

    model = Food
    form_class = FoodCreateServingForm
    success_url = '/'

    def form_valid(self, form):
        data = serving_to_data(form.cleaned_data.get('serving'))
        form.instance.data_value = data.get('data_value')
        form.instance.data_measurement = data.get('data_measurement')
        form.instance.user_created = self.request.user
        form.instance.user_updated = self.request.user
        return super().form_valid(form)


class FoodDetailView(LoginRequiredMixin, TemplateView):
    """
    View to show the following:
    * Detail view of food obj passed into URL.
    * Form to add food to a diary meal.
    * Form to add food to a saved meal.
    """

    template_name = 'food/food_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(Food, slug=self.kwargs['slug'])
        context['diary_form'] = FoodToDiaryForm(
            prefix='diary_form',
            data=self.request.POST if 'diary_form' in self.request.POST else None,
        )
        context['meal_form'] = FoodToMealForm(
            prefix='meal_form',
            data=self.request.POST if 'meal_form' in self.request.POST else None,
            request=self.request,
        )
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if context['diary_form'].is_valid():
            instance = context['diary_form'].save(commit=False)
            instance.user = request.user
            instance.food = context['object']
            instance.save()
            messages.success(request, 'Food added to Diary')

        elif context['meal_form'].is_valid():
            instance = context['meal_form'].save(commit=False)
            instance.user = request.user
            instance.food = context['object']
            instance.save()
            messages.success(request, 'Food added to Meal')

        else:
            messages.error(request, 'An error has occured, please review below and re-submit')

        return self.render_to_response(context)


class FoodUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Food update view with one 'serving' form field to combine and replace
    the two model fields 'data_value' and 'data_measurement'
    E.g. Form: serving: '100g' -> Model: data_value: 100, data_measurement: 'g'
    """

    model = Food
    form_class = FoodCreateServingForm

    def get_initial(self):
        initial = super().get_initial()
        initial['serving'] = data_to_serving(self.object.data_measurement)
        return initial

    def form_valid(self, form):
        data = serving_to_data(form.cleaned_data.get('serving'))
        form.instance.data_value = data.get('data_value')
        form.instance.data_measurement = data.get('data_measurement')
        form.instance.user_updated = self.request.user
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.user_created == self.request.user


class FoodDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Food
    success_url = reverse_lazy('food:list')

    def test_func(self):
        obj = self.get_object()
        return obj.user_created == self.request.user
