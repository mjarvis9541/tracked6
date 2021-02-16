from django.urls import path

from . import views

app_name = 'progress'
urlpatterns = [
    path('', views.ProgressListView.as_view(), name='list'),

]


