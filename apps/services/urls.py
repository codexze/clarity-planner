from django.urls import path
from .views import ServiceView

urlpatterns = [
    path('', ServiceView.as_view(), name='service-list-create'),  # List all services / create new
    path('<int:service_id>/', ServiceView.as_view(), name='service-detail'),  # Retrieve, update, delete
]
