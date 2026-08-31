from django.urls import path
from .views import RegisterView,MyProfileView,LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )

urlpatterns = [
    
      path('register/',RegisterView.as_view(),name='register_view'),
      path('login/',TokenObtainPairView.as_view(),name='login'),
      path('login/refresh/',TokenRefreshView.as_view(),name='refresh'),
      path('profile/',MyProfileView.as_view(),name='profile'),
      path('logout/',LogoutView.as_view(),name='logout'),
 ]
