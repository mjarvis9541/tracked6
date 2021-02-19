from django.shortcuts import redirect, render

from .forms import MealCreateForm
from .models import Meal


def meal_list_view(request):
    template_name = 'meals/meal_list.html'
    context = {}
    context['object_list'] = Meal.objects.filter(user=request.user)
    return render(request, template_name, context)


def meal_create_view(request):
    template_name = 'meals/meal_create.html'
    context = {}

    if request.method == 'POST':
        form = MealCreateForm(request.POST, request=request)
        if form.is_valid():
            request.session['name'] = form.cleaned_data.get('name')
            request.session['description'] = form.cleaned_data.get('description')
            return redirect('meals:add_food')
    else:
        form = MealCreateForm(request=request)

    context['form'] = form
    return render(request, template_name, context)


def meal_add_food_view(request):
    template_name = 'meals/meal_add_food.html'
    context = {}
    return render(request, template_name, context)
