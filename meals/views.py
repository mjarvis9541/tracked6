from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.forms.models import model_to_dict
from food.models import Food

from .forms import MealCreateForm, AddFoodToMealFormSet
from .models import Meal


def meal_list_view(request):
    template_name = 'meals/meal_list.html'
    context = {}
    context['object_list'] = Meal.objects.filter(user=request.user)
    return render(request, template_name, context)


def meal_create_view(request):

    template_name = 'meals/meal_create.html'
    context = {}
    initial_data = {
        'name': request.session.get('name'),
        'description': request.session.get('description'),
    }

    if request.method == 'POST':
        form = MealCreateForm(request.POST, request=request, initial=initial_data)
        if form.is_valid():
            request.session['name'] = form.cleaned_data.get('name')
            request.session['description'] = form.cleaned_data.get('description')
            return redirect('meals:add_food')
    else:
        form = MealCreateForm(request=request, initial=initial_data)

    context['form'] = form
    return render(request, template_name, context)


def meal_add_food_view(request):

    if not request.session.get('name'): # or not request.session.get('description'):
        return redirect('meals:create')

    template_name = 'meals/meal_add_food.html'
    context = {}
    food_list = Food.objects.summary().values()

    if request.method == 'POST':
        formset = AddFoodToMealFormSet(request.POST, initial=food_list)
        if formset.is_valid():
            meal = {
                'user': request.user,
                'name': request.session.get('name'),
                'description': request.session.get('description')
            }
            count = 1
            for form in formset.cleaned_data:
                if form.get('quantity'):
                    if count < 10:
                        meal[f'item_{count}'] = get_object_or_404(Food, id=form.get('id'))
                        meal[f'item_{count}_quantity'] = form.get('quantity')
                        count += 1
            obj = Meal.objects.create(**meal)
            request.session.pop('name')
            request.session.pop('description')
            if 'save' in request.POST:
                messages.success(request, 'Food added')
                return redirect('meals:detail', obj.id)
            elif 'another' in request.POST:
                messages.success(request, 'Food added. You can continue adding food below')
                return redirect('meals:update', obj.id)
    else:
        formset = AddFoodToMealFormSet(initial=food_list)

    context['management_data'] = formset

    paginator = Paginator(formset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['food_list'] = page_obj
    return render(request, template_name, context)



def meal_detail_view(request, pk):
    template_name = 'meals/meal_detail.html'
    context = {}
    context['meal'] = get_object_or_404(Meal, id=pk)
    return render(request, template_name, context)



def meal_update_view(request, pk):
    template_name = 'meals/meal_update.html'
    context = {}

    obj = get_object_or_404(Meal, id=pk)
    meal_items = model_to_dict(obj, exclude=['id', 'user', 'name', 'description'])
    updated_meal_items = {}
    food_list = Food.objects.summary().values()

    if request.method == 'POST':
        formset = AddFoodToMealFormSet(request.POST, initial=food_list)

        if formset.is_valid():
            count = 1
            for item in meal_items:
                if count <= 10:
                    if meal_items[f'item_{count}'] is not None:
                        updated_meal_items[f'item_{count}'] = get_object_or_404(Food, id=meal_items.get(f'item_{count}'))
                        updated_meal_items[f'item_{count}_quantity'] = meal_items[f'item_{count}_quantity']
                        count += 1
                else:
                    messages.error(request, 'You can only add a maximum of 10 items per meal.')
                    break
                for form in formset.cleaned_data:
                    if form.get('quantity'):
                        if count <= 10:
                            updated_meal_items[f'item_{count}'] = get_object_or_404(Food, id=form.get('id'))
                            updated_meal_items[f'item_{count}_quantity'] = form.get('quantity')
                            count += 1
            for attr, value in updated_meal_items.items():
                setattr(obj, attr, value)
                obj.save()
                messages.success(request, 'Food added')
                return redirect('meals:list')

    else:
        formset = AddFoodToMealFormSet(initial=food_list)

    context['meal'] = obj
    context['management_data'] = formset

    paginator = Paginator(formset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['food_list'] = page_obj
    return render(request, template_name, context)


def meal_delete_view(request, pk):
    template_name = 'meals/meal_confirm_delete.html'
    context = {}
    context['meal'] = get_object_or_404(Meal, id=pk)
    return render(request, template_name, context)



