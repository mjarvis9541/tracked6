from django.urls import path

from . import views

app_name = 'diaries'
urlpatterns = [
    # Viewing food in diary
    path('', views.DiaryDayListView.as_view(), name='today'),
    path(
        '<int:year>-<int:month>-<int:day>/',
        views.DiaryDayListView.as_view(),
        name='day',
    ),
    path(
        '<int:year>-<int:month>-<int:day>/meal-detail/<int:meal>/',
        views.DiaryMealListView.as_view(),
        name='meal_list',
    ),
    # Adding food to diary
    path(
        '<int:year>-<int:month>-<int:day>/add-multiple-food-to-diary/<int:meal>/',
        views.DiaryAddMultipleFoodView.as_view(),
        name='create',
    ),
    path(
        '<int:year>-<int:month>-<int:day>/copy-meal/<int:meal>/',
        views.DiaryCopyMealPreviousDay.as_view(),
        name='copy_meal_previous_day',
    ),
    path(
        '<int:year>-<int:month>-<int:day>/copy-all-meal/',
        views.DiaryCopyAllMealPreviousDay.as_view(),
        name='copy_all_meal_previous_day',
    ),
    path(
        '<int:year>-<int:month>-<int:day>/add-meal-to-diary/<int:meal>/',
        views.DiaryAddMealView.as_view(),
        name='browse_saved_meal',
    ),
    path(
        '<int:year>-<int:month>-<int:day>/add-meal-to-diary-confirm/<int:meal>/<uuid:saved_meal>/',
        views.DiaryAddMealConfirmView.as_view(),
        name='saved_meal_to_diary',
    ),
    # Updating food in diary
    path('<uuid:pk>/update/', views.DiaryUpdateView.as_view(), name='update'),
    # Deleting food in diary
    path('<uuid:pk>/confirm-delete/', views.DiaryDeleteView.as_view(), name='delete'),
    path(
        'confirm-delete-multiple/',
        views.DiaryDeleteMultipleView.as_view(),
        name='delete_list',
    ),
]
