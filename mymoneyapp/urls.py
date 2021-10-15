from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("log-in", views.log_in, name="log-in"),
    path("sign-up", views.sign_up, name="sign-up"),
    path("general", views.general, name="general"),
    path("edit-account/<int:id>", views.account, name="account"),
    path("edit-record/<int:id>", views.edit_record, name="edit-record"),
    path("add-account", views.add_account, name="add-account"),
    path("add-record", views.add_record, name="add-record"),
    path("logout", views.logout_view, name="logout")
]
