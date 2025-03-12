from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserView, LogoutView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('current/', UserView.as_view(), name="current_user"),
    path('logout/', LogoutView.as_view(), name='logout'),

]