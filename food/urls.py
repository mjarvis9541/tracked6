from django.urls import path

from .api import views as api_views
from . import views

app_name = 'food'
urlpatterns = [
    path('flv/', views.FoodListed.as_view()),

    path('api/', api_views.FoodListCreateAPIView.as_view(), name='food_listcreate_api'),
    path('api/<uuid:pk>/', api_views.FoodRetrieveUpdateDestroyAPIView.as_view(), name='food_retrieveupdatedelete_api'),

    # Food urls
    path('', views.FoodListView.as_view(), name='list'),    
    path('create/', views.FoodCreateView.as_view(), name='create'),
    path('<uuid:pk>/detail/', views.FoodDetailView.as_view(), name='detail'), 
    path('<uuid:pk>/update/', views.FoodUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.FoodDeleteView.as_view(), name='delete'),

    # Brand urls
    path('brand/list/', views.BrandListView.as_view(), name='brand_list'),    
    path('brand/create/', views.BrandCreateView.as_view(), name='brand_create'),
    path('brand/<uuid:pk>/detail/', views.BrandDetailView.as_view(), name='brand_detail'), 
    path('brand/<uuid:pk>/update/', views.BrandUpdateView.as_view(), name='brand_update'),
    path('brand/<uuid:pk>/delete/', views.BrandDeleteView.as_view(), name='brand_delete'),

    # Category urls
    path('category/list/', views.CategoryListView.as_view(), name='category_list'),    
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<uuid:pk>/detail/', views.CategoryDetailView.as_view(), name='category_detail'), 
    path('category/<uuid:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<uuid:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),


]