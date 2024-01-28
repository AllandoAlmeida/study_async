from django.urls import path
from . import views

urlpatterns = [
    path("create_super_user/", views.create_super_user, name="create_super_user"),
    path("register/", views.register, name="register"),
    path("logar/", views.logar, name="login"),
    path("logout/", views.logout, name="logout"),
]
