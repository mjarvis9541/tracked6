from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import EmailMessage
from .forms import UserCreationForm
from django.template.loader import render_to_string
""" Authentication """


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    template_name = 'accounts/logout.html'


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'emails/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


""" Registration """


class RegisterView(CreateView):
    """
    Standard registration view, takes full name, username, email, password1 & password2.
    """

    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('profiles:profile')

    def dispatch(self, request, *args, **kwargs):
        # overriding dispatch overrides all methods (get, post, etc)
        if request.user.is_authenticated:
            messages.error(
                request,
                'You are already registered. If you wish to create a new \
                    account, please log out and try again.',
            )
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_ = super().form_valid(form)
        login(self.request, self.object)
        return user_
