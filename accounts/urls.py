
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as account_views
from .forms import AuthenticationForm

app_name = "accounts"
urlpatterns = [
    path('register/', account_views.UserRegistration.as_view(), name="register"),
    path('login/', auth_views.login,
                  {'template_name': 'accounts/login.html',
                   'authentication_form': AuthenticationForm}, name='login'),
    path('logout', auth_views.logout, name='logout'),
]
