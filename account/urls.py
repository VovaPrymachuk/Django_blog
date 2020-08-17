from django.urls import path
from django.contrib.auth import views as auth_views

from account.views import *

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register_url'),
    path('login/', LoginView.as_view(), name='login_url'),
    path('logout/', LogoutUser.as_view(), name='logout_url'),
    path(
        'confirm_email/<str:user_id>/<str:token>',
        RegisterConfirmView.as_view(),
        name='confirm_email'
    ),
    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/reset_password.html',
            html_email_template_name='accounts/reset_password_email.html',
            success_url=settings.LOGIN_URL,
            token_generator=user_tokenizer),
        name='reset_password'
        ),
    path(
        'reset-password-confirmation/<str:uidb64>/<str:token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/reset_password_update.html',
            post_reset_login=True,
            post_reset_login_backend='django.contrib.auth.backends.ModelBackend',
            token_generator=user_tokenizer,
            success_url=settings.LOGIN_REDIRECT_URL),
        name='password_reset_confirm'
    ),
    path('profile/<str:username>/', UserProfile.as_view(), name='user_profile'),
]
