from django.urls import path

from . import views

app_name = 'diaries'
urlpatterns = [
    # Listing diary food entries for today
    path(
        '', 
        views.DiaryDayListView.as_view(), 
        name='today'),
    # Listing diary food entries for a given day
    path(
        '<int:year>-<int:month>-<int:day>/',
        views.DiaryDayListView.as_view(),
        name='day',
    ),
    # Detail view of a diary meal (breakfast, morning snack, lunch, etc.)
    path(
        '<int:year>-<int:month>-<int:day>/meal-detail/<int:meal>/',
        views.DiaryMealDetailView.as_view(),
        name='meal_detail',
    ),
    # Adding multiple diary food entries in a single view - formset
    path(
        '<int:year>-<int:month>-<int:day>/add-multiple-food-to-diary/<int:meal>/',
        views.DiaryAddMultipleFoodView.as_view(),
        name='create',
    ),
    # Adding multiple diary food entries in a single view - formset
    # path(
    #     '<int:year>-<int:month>-<int:day>/add-multiple-food-to-diary/<int:meal>/',
    #     views.diary_add_multiple_food_view,
    #     name='create',
    # ),
    # Copying diary food entries from a single meal on a previous day
    path(
        '<int:year>-<int:month>-<int:day>/copy-meal/<int:meal>/',
        views.DiaryMealCopyPreviousDay.as_view(),
        name='copy_meal_previous_day',
    ),
    # path(
    #     '<int:year>-<int:month>-<int:day>/copy-meal/<int:meal>/',
    #     views.diary_copy_meal_from_previous_day_view,
    #     name='copy_meal_previous_day',
    # ),
    # Copying diary food entries from all meals on a previous day
    path(
        '<int:year>-<int:month>-<int:day>/copy-all-meals/',
        views.diary_copy_all_meals_from_previous_day_view,
        name='copy_all_meals_previous_day',
    ),
    # Updating a single diary food entry
    path('<uuid:pk>/update/', views.diary_update_view, name='update'),
    # Deleting a single diary food entry
    path('<uuid:pk>/confirm-delete/', views.DiaryDeleteView.as_view(), name='delete'),
    # Deleting multiple diary food entries
    path('confirm-delete-multiple/', views.diary_delete_multiple_food_view, name='delete_list'),
    # Adding a saved meal to food diary - selecting the meal to add
    # Saved meal is a collection of food and associated quantities
    path(
        '<int:year>-<int:month>-<int:day>/add-meal-to-diary/<int:meal>/',
        views.DiaryAddMealView.as_view(),
        name='browse_saved_meal',
    ),
    # path(
    #     '<int:year>-<int:month>-<int:day>/add-meal-to-diary/<int:meal>/',
    #     views.diary_add_meal_view,
    #     name='browse_saved_meal',
    # ),
    # Adding a saved meal to the food diary - confirmation view
    path(
        '<int:year>-<int:month>-<int:day>/add-meal-to-diary-confirm/<int:meal>/<uuid:saved_meal>/',
        views.diary_add_meal_confirm_view,
        name='saved_meal_to_diary',
    ),
]
