from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from blog.models import Post, Tag
from blog.forms import CreateUserForm


def register_page(request):
    if request.user.is_authenticated:
        return redirect('posts_list_url')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for {}'.format(user))
                return redirect(login_page, messages)

        context = {'form': form}
        return render(request, 'blog/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('posts_list_url')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('posts_list_url')
            else:
                messages.info(request, 'Username OR Password is not correct!')

        context = {}
        return render(request, 'blog/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login_url')


@login_required(login_url='login_url')
def posts_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


@login_required(login_url='login_url')
def post_detail(request, slug):
    post = Post.objects.get(slug__iexact=slug)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='login_url')
def tags_list(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'blog/tags_list.html', context)


@login_required(login_url='login_url')
def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    context = {'tag': tag}
    return render(request, 'blog/tag_detail.html', context)
