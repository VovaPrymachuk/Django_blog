from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from .models import Post, Tag
from .forms import CreateUserForm, PostForm, TagForm
from .utils import ObjectDetailMixin, ObjectUpdateMixin, ObjectListMixin


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


class PostsList(ObjectListMixin, View):
    model = Post
    template = 'blog/index.html'


class PostCreate(View):
    def get(self, request):
        form = PostForm()
        context = {'form': form}
        return render(request, 'blog/create_post.html', context)

    def post(self, request):
        bound_form = PostForm(request.POST)
        print(943)
        if bound_form.is_valid():
            entry = bound_form.save(commit=False)
            entry.author = request.user
            entry.save()
            print(12131)
            return redirect('posts_list_url')

        context = {'form': bound_form}
        return render(request, 'blog/create_post.html', context)


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostUpdate(ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update.html'


class TagsList(ObjectListMixin, View):
    model = Tag
    template = 'blog/tags_list.html'


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(View):
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


class TagUpdate(ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update.html'
