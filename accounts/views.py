from django import template
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import ResendActivationEmailForm, UserCreationForm


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    # redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    template_name = 'accounts/logout.html'


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class RegisterView(CreateView):
    """
    Standard registration view, takes full name, username, email,
    password1 & password2.
    """

    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')

    # def dispatch(self, request, *args, **kwargs):
    #     # overriding dispatch overrides all methods (get, post, etc)
    #     if request.user.is_authenticated:
    #         messages.error(
    #             request,
    #             'You are already registered. If you wish to create a new account, please log out and try again.',
    #         )
    #         return redirect(self.success_url)
    #     return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # self.send_email(form.cleaned_data)
        user_ = super().form_valid(form)
        login(self.request, self.object)
        return user_

    # def send_email(self, valid_data):
    #     print(valid_data)
    #     email = EmailMessage()
    #     return email.send()


class AccountView(LoginRequiredMixin, TemplateView):
    """ Main page for account settings """

    template_name = 'accounts/index.html'


class ChangeNameView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'accounts/change_name.html'
    fields = ['first_name', 'last_name']
    success_message = 'Your name has been updated'
    success_url = reverse_lazy('accounts:account')

    def get_object(self):
        return self.request.user


class ChangeEmailView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'accounts/change_email.html'
    fields = ['email']
    success_message = 'Your email address has been updated'
    success_url = reverse_lazy('accounts:account')

    def get_object(self):
        return self.request.user


class ChangeUsernameView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'accounts/change_username.html'
    fields = ['username']
    success_message = 'Your username has been updated'
    success_url = reverse_lazy('accounts:account')

    def get_object(self):
        return self.request.user


from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User


def register(request):
    template_name = 'accounts/register.html'
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            domain = current_site.domain  # new
            site_name = current_site.name  # new
            email_body = render_to_string(
                'accounts/account_activation_email.html',
                {
                    'user': user,
                    # 'domain': current_site.domain,
                    'domain': domain,  # new
                    'site_name': site_name,  # new
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                },
            )
            email = form.cleaned_data.get('email')
            activation_email = EmailMessage(
                subject='Activate your account',
                body=email_body,
                from_email='\'Trackedfitness\' <noreply@trackedfitness.com>',
                to=[email],
            )
            activation_email.send()
            return redirect('accounts:account_activation_sent')
    else:
        form = UserCreationForm()
    context['form'] = form
    return render(request, template_name, context)


def account_activation_resend(request):
    """
    This view enables the user to resend the activation email if they
    didn't receive it or the link expired.
    """
    template_name = 'accounts/account_activation_resend.html'
    context = {}
    if request.method == 'POST':
        form = ResendActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            current_site = get_current_site(request)
            domain = current_site.domain
            site_name = current_site.name
            email_body = render_to_string(
                'accounts/account_activation_email.html',
                {
                    'user': user,
                    'domain': domain,
                    'site_name': site_name,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                },
            )
            activation_email = EmailMessage(
                subject='Activate your account',
                body=email_body,
                from_email='\'Trackedfitness\' <noreply@trackedfitness.com>',
                to=[email],
            )
            activation_email.send()
            return redirect('accounts:account_activation_sent')
    else:
        form = ResendActivationEmailForm()
    context['form'] = form
    return render(request, template_name, context)


def account_activation_sent(request):
    template_name = 'accounts/account_activation_sent.html'
    return render(request, template_name, {})


def activate_account(request, uidb64, token):
    template_name = 'accounts/account_activation_invalid.html'
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        # user = User._default_manager.get(pk=uid)
        user = User.objects.get(pk=uid)  # new
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:account_activation_complete')
    return render(request, template_name, {})


def account_activation_complete(request):
    template_name = 'accounts/account_activation_complete.html'
    return render(request, template_name, {})
