from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
    View,
    TemplateView,
)
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from .forms import FoodToDiaryForm, FoodToMealForm
from .forms import (
    BrandCreateForm,
    FoodCreateServingForm,
    FoodDetailToDiaryForm,
    BrandFilterForm,
    FoodFilterForm,
)
from .mixins import BrandFilterMixin, FoodFilterMixin
from .models import Brand, Category, Food
from .utils import data_to_serving, serving_to_data
from django.urls import reverse


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


# class FoodDisplay(DetailView):
#     model = Food

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = FoodDetailToDiaryForm()
#         return context


# class FoodDetailForm(SingleObjectMixin, FormView):
#     template_name = 'food/food_detail.html'
#     form_class = FoodDetailToDiaryForm
#     model = Food

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         return super().post(request, *args, **kwargs)

#     def form_valid(self, form):
#         self.date = form.cleaned_data.get('date')
#         form.instance.user = self.request.user
#         form.instance.food = self.object
#         form.save()
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('diaries:day', kwargs={'year': self.date.year, 'month': self.date.month, 'day': self.date.day})


# class FoodDetailView(View):
#     def get(self, request, *args, **kwargs):
#         view = FoodDisplay.as_view()
#         return view(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         view = FoodDetailForm.as_view()
#         return view(request, *args, **kwargs)




class FoodDetailView(TemplateView):
    template_name = 'food/food_detail.html'

    def get(self, request, *args, **kwargs):
        self.context['obj'] = get_object_or_404(Food, id=self.kwargs.get('pk'))
        self.context['diary_form'] = FoodToDiaryForm(prefix='diary')
        self.context['meal_form'] = FoodToMealForm(prefix='meal', request=request)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        self.context['obj'] = get_object_or_404(Food, id=self.kwargs.get('pk'))
        self.context['diary_form'] = FoodToDiaryForm(request.POST, prefix='diary')
        self.context['meal_form'] = FoodToMealForm(
            request.POST, prefix='meal', request=request
        )

        return render(request, self.template_name, self.context)


def food_detail_view(request, pk):
    """
    View to show the following:
    * Detail view of food obj passed into URL.
    * Form to add food to a diary meal.
    * Form to add food to a saved meal.
    """
    template_name = 'food/food_detail.html'
    context = {}

    obj = get_object_or_404(Food, id=pk)
    diary_form = FoodToDiaryForm(prefix='diary')
    meal_form = FoodToMealForm(prefix='meal', request=request)

    # Food to Diary Meal
    if request.method == 'POST' and 'food_to_diary' in request.POST:
        diary_form = FoodToDiaryForm(request.POST, prefix='diary')
        if diary_form.is_valid():
            form = diary_form.save(commit=False)
            form.user = request.user
            form.food = obj
            form.save()
    else:
        diary_form = FoodToDiaryForm(prefix='diary')

    # Food to Saved Meal
    if request.method == 'POST' and 'food_to_meal' in request.POST:
        meal_form = FoodToMealForm(request.POST, request=request, prefix='meal')
        if meal_form.is_valid():
            form = meal_form.save(commit=False)
            form.user = request.user
            form.food = obj
            form.save()
    else:
        meal_form = FoodToMealForm(prefix='meal', request=request)

    context['obj'] = obj
    context['diary_form'] = diary_form
    context['meal_form'] = meal_form
    return render(request, template_name, context)


class FoodDetailView(TemplateView):
    ### TemplateResponseMixin
    template_name = 'food/food_detail.html'

    ### ContextMixin 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(Food, id=self.kwargs['pk'])
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
