from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'services', views.ServiceView, basename='services')
router.register(r'service-types', views.ServiceTypeView, basename='service-types')
router.register(r'addons', views.AddonView, basename='addons')

urlpatterns = []

urlpatterns += router.urls
