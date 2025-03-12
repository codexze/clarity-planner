from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'namespace', views.ServiceView, basename='services')
router.register(r'service_types', views.ServiceTypeView, basename='service_types')
router.register(r'employee', views.StaffView, basename='employee')

urlpatterns = []

urlpatterns += router.urls
