from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'clients', views.ClientView, basename='clients')
router.register(r'genders', views.GenderView, basename='genders')
router.register(r'companies', views.CompanyView, basename='companies')
router.register(r'known-addresses', views.KnownAddressView, basename='known-addresses')

urlpatterns = []

urlpatterns += router.urls

