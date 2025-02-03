from django.urls import path
from .views import GenderView, ClientView

urlpatterns = [
    path('', ClientView.as_view(), name='client-list-create'),  # List all clients / create new
    path('<int:client_id>/', ClientView.as_view(), name='client-detail'),  # Retrieve, update, delete
    path('genders/', GenderView.as_view(), name='gender-list'), # List all clients
    path('genders/<str:gender_value>/', GenderView.as_view(), name='gender-detail') # Retrieve
]   
