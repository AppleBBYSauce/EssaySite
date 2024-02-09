# Item's name: urls
# Autor: bby
# DateL 2024/2/5 1:44
from django.urls import path

from . import views

urlpatterns = [
    path("", views.mainSite, name="index"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("visible", views.changeVisible, name="visible"),
    path("delete", views.deleteArticle, name="delete"),
    path("manage", views.manage, name="manage"),
    path("register", views.user_register, name="register"),
    path("upload", views.upload, name="upload"),
    path("download", views.returnFile, name="download"),
    path("view", views.view_content, name="view"),
    path("theme", views.createTheme, name="theme"),
]
