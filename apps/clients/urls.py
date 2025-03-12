from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'namespace', views.ClientView, basename='clients')
router.register(r'genders', views.GenderView, basename='genders')

urlpatterns = []

urlpatterns += router.urls

