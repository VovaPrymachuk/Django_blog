from django.contrib.auth import views
from django.urls import path

from account.views import RegisterUser, LoginUser, LogoutUser, UserProfile

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register_url'),
    path('login/', LoginUser.as_view(), name='login_url'),
    path('logout/', LogoutUser.as_view(), name='logout_url'),
    path('profile/<str:username>/', UserProfile.as_view(), name='user_profile'),
]
