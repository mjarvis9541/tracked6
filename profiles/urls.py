from django.urls import path

from . import test_views as views

app_name = 'profiles'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:year>/<int:month>/<int:day>', views.ProfileView.as_view(), name='profile_year'),
    path('newprofile/<int:hello>/', views.NewProfile.as_view()),

    # path('temps/', views.TemplatePostView.as_view(), name='template_post'),
]