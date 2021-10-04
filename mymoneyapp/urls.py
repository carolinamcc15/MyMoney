from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("log-in", views.login, name="log-in"),
    path("sign-up", views.sign_up, name="sign-up"),
    path("general", views.general, name="general"),
]