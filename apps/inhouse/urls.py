from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'services', views.ServiceView, basename='services')
router.register(r'service_types', views.ServiceTypeView, basename='service_types')
router.register(r'addons', views.AddonView, basename='addons')
router.register(r'staff', views.StaffView, basename='staff')

urlpatterns = []

urlpatterns += router.urls
