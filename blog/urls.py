from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('<slug:slug>/detail', views.PostDetailView.as_view(), name='detail'),
    path('<slug:slug>/update', views.PostUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete', views.PostDeleteView.as_view(), name='Delete'),
]
