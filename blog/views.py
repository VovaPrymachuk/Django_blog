from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import View

from .models import Post, Tag
from .forms import CreateUserForm, PostForm, TagForm
from .utils import ObjectDetailMixin, ObjectUpdateMixin, ObjectListMixin, ObjectDeleteMixin


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


class UserProfile(LoginRequiredMixin, View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        context = {'user': user}
        return render(request, 'blog/user_profile.html', context)


class PostsList(ObjectListMixin, View):
    model = Post
    template = 'blog/index.html'


class PostCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        context = {'form': form}
        return render(request, 'blog/create_post.html', context)

    def post(self, request):
        bound_form = PostForm(request.POST)
        if bound_form.is_valid():
            entry = bound_form.save(commit=False)
            entry.author = request.user
            entry.save()
            return redirect('posts_list_url')

        context = {'form': bound_form}
        return render(request, 'blog/create_post.html', context)


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update.html'


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    get_template = 'blog/post_delete.html'
    post_template = 'posts_list_url'


class TagsList(ObjectListMixin, View):
    model = Tag
    template = 'blog/tags_list.html'


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = TagForm()
        context = {'form': form}
        return render(request, 'blog/tag_create.html', context)

    def post(self, request):
        form = TagForm(request.POST)
        if form.is_valid():
            new_tag = form.save()
            return redirect(new_tag)

        context = {'form': form}
        return render(request, 'blog/tag_create.html', context)


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update.html'


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    get_template = 'blog/tag_delete.html'
    post_template = 'tags_list_url'
