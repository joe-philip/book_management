from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('', views.AuthorsAPI, basename='authors')

urlpatterns = []+router.urls
