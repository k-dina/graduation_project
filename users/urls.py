from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("new_user/", views.new_user, name="new_user"),
    path("logout/", views.logout_view, name="logout"),

]
