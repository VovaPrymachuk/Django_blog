from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from .models import Post, Tag
from .forms import CreateUserForm, CreatePostForm, TagCreateForm
from .utils import ObjectDetailMixin


def register_page(request):
    if request.user.is_authenticated:
        return redirect('posts_list_url')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(login_page)

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


def posts_lists(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


class PostCreate(View):

    def get(self, request):
        form = CreatePostForm()
        tags = Tag.objects.all()
        context = {'form': form, 'tags': tags}
        return render(request, 'blog/create_post.html', context)

    # def post(self, request):
    #     form = CreatePostForm(request.POST)
    #     tags = Tag.objects.all()
    #     print(943)
    #     if form.is_valid():
    #         entry = form.save(commit=False)
    #         entry.author = request.user
    #         new_post = entry.save()
    #         print(12131)
    #         return redirect('posts_list_url')
    #
    #     context = {'form': form, 'tags': tags}
    #     return render(request, 'blog/create_post.html', context)


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


def tags_list(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'blog/tags_list.html', context)


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(View):
    def get(self, request):
        form = TagCreateForm()
        context = {'form': form}
        return render(request, 'blog/tag_create.html', context)

    def post(self, request):
        form = TagCreateForm(request.POST)
        if form.is_valid():
            new_tag = form.save()
            return redirect(new_tag)

        context = {'form': form}
        return render(request, 'blog/tag_create.html', context)
