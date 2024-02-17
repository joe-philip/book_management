from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('review', views.ReviewsAPI, basename='review')

urlpatterns = [
    path('signup', views.SignupAPI.as_view()),
    path('login', views.LoginAPI.as_view())
]+router.urls
