from django.urls import path
from .views import *

urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('register/', register_page, name='register_page_url'),
    path('login/', login_page, name='login_url'),
    path('logout/', logout_user, name='logout_url'),
    path('post/<str:slug>/', post_detail, name='post_detail_url'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tags/<str:slug>', tag_detail, name='tag_detail_url'),
]
