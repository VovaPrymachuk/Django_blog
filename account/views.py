from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View

from account.forms import CreateUserForm


class RegisterUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('posts_list_url')
        else:
            form = CreateUserForm()
            context = {'form': form}
            return render(request, 'account/register.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')

        context = {'form': form}
        return render(request, 'account/register.html', context)


class LoginUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('posts_list_url')
        return render(request, 'account/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts_list_url')
        else:
            messages.info(request, 'Username OR Password is not correct!')

        return render(request, 'account/login.html')


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('login_url')


class UserProfile(LoginRequiredMixin, View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        context = {'user': user}
        return render(request, 'account/user_profile.html', context)
