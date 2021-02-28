from django.urls import path

from . import views

app_name = 'meals'
urlpatterns = [
    path('', views.MealListView.as_view(), name='list'),
    path('create/', views.MealCreateView.as_view(), name='create'),
    path(
        '<uuid:meal_id>/add-food/',
        views.MealItemCreateStep1View.as_view(),
        name='meal_add_1',
    ),
    path(
        '<uuid:meal_id>/add/<uuid:food_id>/',
        views.MealItemCreateStep2View.as_view(),
        name='meal_add_2',
    ),
    # path('<uuid:pk>/detail/', views.MealDetailView.as_view(), name='detail'),
    path('<uuid:pk>/delete/', views.MealDeleteView.as_view(), name='delete'),
    path('<uuid:pk>/list/', views.MealItemListView.as_view(), name='item_list'),
    path(
        '<uuid:pk>/meal-item-delete/',
        views.MealItemDeleteView.as_view(),
        name='item_delete',
    ),
]
