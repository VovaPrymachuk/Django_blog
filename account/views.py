from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, reverse
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View

from account.forms import RegistrationForm
from account.utils import user_tokenizer


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            token = user_tokenizer.make_token(user)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            url = 'http://localhost:8000' + reverse('confirm_email', kwargs={'user_id': user_id, 'token': token})
            message = get_template('accounts/register_email.html').render({
              'confirm_url': url
            })
            mail = EmailMessage('Django Blog app Email Confirmation', message,
                                to=[user.email],
                                from_email=settings.EMAIL_HOST_USER)
            mail.content_subtype = 'html'
            mail.send()

            context = {
                'form': AuthenticationForm,
                'message': 'A confirmation email has been sent to {}.'
                           'Please confirm to finish registering'.format(user.email)
            }
            return render(request, 'accounts/login.html', context)

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


class RegisterConfirmView(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))

        user = User.objects.get(pk=user_id)

        context = {
            'form': AuthenticationForm(),
            'message': 'Registration confirmation error . '
                       'Please click the reset password to generate '
                       'a new confirmation email.'
        }

        if user and user_tokenizer.check_token(user, token):
            user.is_valid = True
            user.save()
            context['message'] = 'Registration complete. Please login.'

        return render(request, 'accounts/login.html', context)


class LoginView(View):
    def get(self, request):
        context = {'form': AuthenticationForm}
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is None:
                context = {'form': form, 'invalid_creds': True}
                return render(request, 'accounts/login.html', context)

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                context = {'form': form, 'invalid_creds': True}
                return render(request, 'accounts/login.html', context)

            login(request, user)

        return redirect(reverse('posts_list_url'))


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('login_url')


class UserProfile(LoginRequiredMixin, View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        context = {'user': user}
        return render(request, 'accounts/user_profile.html', context)
