from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.UserRegistrationView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),
    path('change-password/',views.UserChangePasswordView.as_view(),name='change_password'),
]
