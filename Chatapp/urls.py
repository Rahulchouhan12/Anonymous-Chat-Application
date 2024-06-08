"""Chatapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from chats import views


admin.site.site_header = 'Anonymous Chat Application'
admin.site.site_title = 'Admin Panel'
admin.site.index_title = 'Welcome to IncognitoSphere Administration Panel'


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.Home),
    path("login",views.login),
    path("login/Globalchat/<int:key>/",views.Globalchat,name="Globalchat"),
    path("login/Globalchat//chats<int:key>/<str:rkey>/",views.privateChat,name="privateChat"),
    path("delete_entry/<str:key>/<int:msgid>",views.delete_entry,name="delete_entry"),
    path("delete_entry2/<str:key>/<str:rkey>/<int:msgid>",views.delete_entry2,name="delete_entry2"),
    path("/Profile/<int:key>",views.Profile, name="Profile"),
    path("about",views.about),
    path("services",views.services),
    path("signup/",views.signup),
    path("block_chatter/<int:key>/<str:rkey>",views.block, name="block_chatter"),
    path("unblock/<int:key>/<int:uid>",views.unblock,name="unblock"),
]
