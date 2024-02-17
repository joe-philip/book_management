from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.SignupAPI.as_view()),
    path('login', views.LoginAPI.as_view())
]
