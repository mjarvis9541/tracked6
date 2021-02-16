from django.urls import path

from . import views


app_name = 'diaries'
urlpatterns = [
    path('meal_update/<int:year>-<int:month>-<int:day>/<int:meal>/', views.diary_meal_update_view, name='dmu'),

    # Diary list urls
    path('', views.DiaryDayListView.as_view(), name='today'),
    path('<int:year>-<int:month>-<int:day>/', views.DiaryDayListView.as_view(), name='day'),
    path('<int:year>-<int:month>-<int:day>/meal/<int:meal>/', views.DiaryMealListView.as_view(), name='meal_list'),

    

    path('<int:year>-<int:month>-<int:day>/add-food-to-meal/<int:meal>/', views.add_to_diary_view, name='create'),
    
    path('confirm-delete/', views.diary_delete_list_view, name='delete_list'),
    
    # path('add/<int:year>-<int:month>-<int:day>/<int:meal>/', views.AddToDiaryView.as_view(), name='create'),

    # Update diary entry
    path('<uuid:pk>/update/', views.diary_update_view, name='update'),

    # path('<uuid:pk>/detail/', views.DiaryDetailView.as_view(), name='detail'),
    # path('<uuid:pk>/update/', views.DiaryUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.DiaryDeleteView.as_view(), name='delete'),


    # Diary create urls
    # path('<int:year>-<int:month>-<int:day>/add-food-to-meal/<int:meal>/', views.add_to_diary_view, name=''),
]





    