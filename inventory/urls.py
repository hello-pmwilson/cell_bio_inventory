from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_data", views.get_data, name="get_data"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("skeleton/", views.skeleton, name="skeleton")
]