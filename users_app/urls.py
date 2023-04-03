from django.urls import path, include
from django.contrib.auth import views as auth_views
from. forms import CustomLoginForm
from . import views
urlpatterns = [
    path('login/', auth_views.LoginView.as_view( authentication_form=CustomLoginForm,template_name='registration/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout_'),
    path('register/', views.register, name = 'register'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]