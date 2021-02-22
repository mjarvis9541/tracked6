from django.urls import path

from . import views

app_name = 'diaries'
urlpatterns = [
    path(
        'browse-saved-meals/<int:year>-<int:month>-<int:day>/<int:meal>/',
        views.browse_saved_meals_view, 
        name='browse_saved_meal',
    ),

    path(
        'add-saved-meal/<int:year>-<int:month>-<int:day>/<int:meal>/<uuid:saved_meal>/',
        views.add_saved_meal_to_diary_view, 
        name='saved_meal_to_diary',
    ),



    path('meal_update/<int:year>-<int:month>-<int:day>/<int:meal>/',views.diary_meal_update_view,name='dmu'),
    
    path('', views.DiaryDayListView.as_view(), name='today'),
    path('<int:year>-<int:month>-<int:day>/', views.DiaryDayListView.as_view(), name='day'),
    
    path('<int:year>-<int:month>-<int:day>/meal/<int:meal>/',views.DiaryMealListView.as_view(),name='meal_list'),



    path('<int:year>-<int:month>-<int:day>/add-food-to-diary/<int:meal>/',views.add_to_diary_view,name='create'),

    # path('<int:year>-<int:month>-<int:day>/add-to-diary/<int:meal>/',views.AddFoodToDiaryView.as_view(), name='create'),
    
    path('<int:year>-<int:month>-<int:day>/copy-meal/<int:meal>/',views.copy_meal_from_previous_day_view,name='copy_meal_previous_day'),
    path('<int:year>-<int:month>-<int:day>/copy-all-meals/',views.copy_all_meals_from_yesterday_view,name='copy_all_meals_previous_day'),
    
    path('<uuid:pk>/update/', views.diary_update_view, name='update'),
    path('<uuid:pk>/delete/', views.DiaryDeleteView.as_view(), name='delete'),
    path('confirm-delete-all/', views.diary_delete_list_view, name='delete_list'),
    
    
    # path('add/<int:year>-<int:month>-<int:day>/<int:meal>/', views.AddToDiaryView.as_view(), name='create'),
    # Update diary entry
    # path('<uuid:pk>/detail/', views.DiaryDetailView.as_view(), name='detail'),
    # path('<uuid:pk>/update/', views.DiaryUpdateView.as_view(), name='update'),
    # Diary create urls
    # path('<int:year>-<int:month>-<int:day>/add-food-to-meal/<int:meal>/', views.add_to_diary_view, name=''),
]
