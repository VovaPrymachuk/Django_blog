from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from .models import Post, Tag
from .forms import PostForm, TagForm
from .utils import ObjectDetailMixin, ObjectUpdateMixin, ObjectListMixin, \
    ObjectDeleteMixin, ObjectCreateMixin


class PostsList(ObjectListMixin, View):
    model = Post
    template = 'blog/index.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/create_post.html'
    redirect_url = 'posts_list_url'


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


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'
    redirect_url = 'tags_list_url'


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update.html'


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    get_template = 'blog/tag_delete.html'
    post_template = 'tags_list_url'
