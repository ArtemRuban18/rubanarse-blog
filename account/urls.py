from django.urls import path
from account.views import register, password_reset
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('login/',auth_view.LoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/',auth_view.LogoutView.as_view(), name = 'logout'),
    path('register/', register, name = 'register'),
    path('password-reset/',password_reset, name='password_reset'),
    path('password-reset-done/',  auth_view.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',  auth_view.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset-complete/',  auth_view.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
]