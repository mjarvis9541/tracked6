from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView, UpdateView, FormView

from .forms import ResendActivationEmailForm, UserCreationForm, UserChangeEmailForm
from .models import User


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


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


class AccountView(LoginRequiredMixin, TemplateView):
    """ Main page for account settings. """

    template_name = 'accounts/index.html'


class NameChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """ Allows the user to change their first and last name. """

    template_name = 'accounts/name_change_form.html'
    fields = ['first_name', 'last_name']
    success_message = 'Your name has been updated'
    success_url = reverse_lazy('accounts:account')

    def get_object(self):
        return self.request.user


class UsernameChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """ Allows the user to change their username. """

    template_name = 'accounts/username_change_form.html'
    fields = ['username']
    success_message = 'Your username has been updated'
    success_url = reverse_lazy('accounts:account')

    def get_object(self):
        return self.request.user


class EmailChangeView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """ Allows the user to change their email address, requires email confirmation. """

    template_name = 'accounts/email_change_form.html'
    form_class = UserChangeEmailForm
    success_message = (
        'We have sent you a link to verify your new email address, please check your inbox and spam/junk folder'
    )
    success_url = reverse_lazy('accounts:email_change_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = self.request.user
        user.email_change_pending = email
        user.save()
        current_site = get_current_site(self.request)
        domain = current_site.domain
        site_name = current_site.name
        email_body = render_to_string(
            'accounts/email_change_email.html',
            {
                'user': user,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            },
        )
        email_message = EmailMessage(
            subject='Confirm email address change',
            body=email_body,
            from_email='\'Trackedfitness\' <noreply@trackedfitness.com>',
            to=[email],
        )
        email_message.send()
        return super().form_valid(form)


def email_change_done_view(request):
    """ Displays a success message for the above. """

    template_name = 'accounts/email_change_done.html'
    return render(request, template_name, {})


def email_change_confirm_view(request, uidb64, token):
    """ Allows the user to change their email address from link within email. """

    template_name = 'accounts/email_change_invalid.html'
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        new_email_address = user.email_change_pending
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.email = new_email_address
        user.email_change_pending = None
        user.save()
        # messages.success(request, 'Your email address been updated')
        return redirect('accounts:email_change_complete')
    return render(request, template_name, {})


def email_change_complete_view(request):
    """ Displays a success message for the above. """

    template_name = 'accounts/email_change_complete.html'
    return render(request, template_name, {})


def register_view(request):
    """ Account registration view, requires email confirmation. """

    template_name = 'accounts/register.html'
    context = {}

    if request.user.is_authenticated:
        messages.error(
            request,
            'You are already registered. If you wish to create a new account, please log out and try again.',
        )
        return redirect('accounts:account')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
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
            email = form.cleaned_data.get('email')
            activation_email = EmailMessage(
                subject='Activate your account',
                body=email_body,
                from_email='\'Trackedfitness\' <noreply@trackedfitness.com>',
                to=[email],
            )
            activation_email.send()
            return redirect('accounts:account_activation_done')
    else:
        form = UserCreationForm()

    context['form'] = form
    return render(request, template_name, context)


def account_activation_view(request):
    """ 
    Allows the user to resend account activation email.
    TODO: Only allow users who aren't banned to access this view
    """
    template_name = 'accounts/account_activation_form.html'
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
            return redirect('accounts:account_activation_done')
    else:
        form = ResendActivationEmailForm()

    context['form'] = form
    return render(request, template_name, context)


def account_activation_done_view(request):
    """ Displays a success message for the above. """

    template_name = 'accounts/account_activation_done.html'
    return render(request, template_name, {})


def account_activation_confirm_view(request, uidb64, token):
    """ Allows the user to activate their account from link within email. """

    template_name = 'accounts/account_activation_invalid.html'
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:account_activation_complete')
    return render(request, template_name, {})


def account_activation_complete_view(request):
    """ Displays a success message for the above. """

    template_name = 'accounts/account_activation_complete.html'
    return render(request, template_name, {})
