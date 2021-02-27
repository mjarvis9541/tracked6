from django.urls import path

from . import views

app_name = 'progress'
urlpatterns = [
    path('', views.ProgressListView.as_view(), name='list'),
    path('create/', views.ProgressCreateView.as_view(), name='create'),
    path('<uuid:pk>/detail/', views.ProgressDetailView.as_view(), name='detail'),
    path('<uuid:pk>/update/', views.ProgressUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.ProgressDeleteView.as_view(), name='delete'),
]


