from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'appointments', views.AppointmentView, basename='appointments')
router.register(r'blocked', views.BlockedTimeView, basename='blocked')
router.register(r'reminders', views.ReminderView, basename='reminders')

urlpatterns = []

urlpatterns += router.urls
