from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'employees', views.EmployeeView, basename='employees')

urlpatterns = []

urlpatterns += router.urls
