"""chatapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from messagesapp import views as messages_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', messages_views.IndexView.as_view(), name="index"),
    path('users/', login_required(messages_views.UserListView.as_view()), name="users-list"),
    path('get-messages/', login_required(messages_views.ConversationView.as_view()), name="get-messages"),
    path('post-message/', login_required(messages_views.MessageView.as_view()), name="post-message"),
    path('accounts/', include("accounts.urls"), name="accounts")
]