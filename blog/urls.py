from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list_url'),
    path('register/', register_page, name='register_page_url'),
    path('login/', login_page, name='login_url'),
    path('logout/', logout_user, name='logout_url'),
    path('post/create/', PostCreate.as_view(), name='post_create_url'),
    path('post/update/<str:slug>/', PostUpdate.as_view(), name='post_update_url'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('post/delete/<str:slug>/', PostDelete.as_view(), name='post_delete_url'),
    path('tags/', TagsList.as_view(), name='tags_list_url'),
    path('tags/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('tag/update/<str:slug>/', TagUpdate.as_view(), name='tag_update_url'),
    path('tag/delete/<str:slug>/', TagDelete.as_view(), name='tag_delete_url'),
]
