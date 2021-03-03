from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    # Index
    path('index/', views.AccountView.as_view(), name='account'),
    
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
    
    # Registration
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('profile-setup/', views.ProfileSetupView.as_view(), name='profile_setup'),
    # path('profile-setup-imperial/', views.ProfileSetupImperialView.as_view(), name='profile_setup_imperial'),
    # path('profile-setup-complete/', views.ProfileSetupCompleteView.as_view(), name='profile_setup_complete'),
    
    # # Account management
    # path('account/', views.AccountView.as_view(), name='account'),
    path('account/change-name/', views.ChangeNameView.as_view(), name='change_name'),
    path('account/change-username/', views.ChangeUsernameView.as_view(), name='change_username'),
    path('account/change-email/', views.ChangeEmailView.as_view(), name='change_email'),
    
    # # Profile management
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    # path('profile/update-imperial/', views.ProfileUpdateImperialView.as_view(), name='profile_update_imperial'),
    # path('profile/update-picture/', views.ChangePictureView.as_view(), name='change_picture'),
    
    # # Target management
    # path('target/', views.TargetView.as_view(), name='target'),
    # path('target-set-default/', views.TargetSetDefaultView.as_view(), name='target_set_default'),
    # path('target-set-grams/', views.TargetSetGramView.as_view(), name='target_set_grams'),
    # path('target-set-percent/', views.TargetSetPercentView.as_view(), name='target_set_percent'),

    # Registration with email confirmation
    path('register/', views.register, name='register'),
    path('register/resend-activation-email/', views.account_activation_resend, name='account_activation_resend'),
    path('register/activation-sent/', views.account_activation_sent, name='account_activation_sent'),
    path('register/activate-account/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path(
        'register/account-activation-complete/', views.account_activation_complete, name='account_activation_complete'
    ),
]
