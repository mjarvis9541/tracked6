from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.AccountView.as_view(), name='account'),
    # Authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # Password management - change (when user knows their current password)
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # Password management - reset (when user has forgotten their current password)
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path('password-reset-complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Account management - change name, username
    path('name-change/', views.NameChangeView.as_view(), name='name_change'),
    path('username-change/', views.UsernameChangeView.as_view(), name='username_change'),
    # Account management - change email (requires email confirmation)
    path('email-change/', views.EmailChangeView.as_view(), name='email_change'),
    path('email-change-done/', views.email_change_done_view, name='email_change_done'),
    path(
        'email-change-confirm/<uidb64>/<token>/',
        views.email_change_confirm_view,
        name='email_change_confirm',
    ),
    path('email-change-complete/', views.email_change_complete_view, name='email_change_complete'),
    # Registration and re-request activation email (requires email confirmation)
    path('register/', views.register_view, name='register'),
    path('register/account-activation/', views.account_activation_view, name='account_activation'),
    path('register/account-activation-done/', views.account_activation_done_view, name='account_activation_done'),
    path(
        'register/account-activation-confirm/<uidb64>/<token>/',
        views.account_activation_confirm_view,
        name='account_activation_confirm',
    ),
    path(
        'register/account-activation-complete/',
        views.account_activation_complete_view,
        name='account_activation_complete',
    ),
]
