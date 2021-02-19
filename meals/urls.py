from django.urls import path

from . import views

app_name = 'meals'
urlpatterns = [
    path('', views.meal_list_view, name='list'),
    path('create/', views.meal_create_view, name='create'),
    path('create/add-food/', views.meal_add_food_view, name='add_food'),
]


