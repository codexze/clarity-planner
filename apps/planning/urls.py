from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from apps.services.views import StaffView

router = DefaultRouter()

router.register(r'employees', StaffView, basename='employees')
router.register(r'appointments', views.AppointmentView, basename='appointments')
router.register(r'blocked', views.BlockedView, basename='blocked')

urlpatterns = []

urlpatterns += router.urls
