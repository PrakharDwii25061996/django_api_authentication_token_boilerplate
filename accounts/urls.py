from django.contrib import admin
from django.urls import path
from accounts import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
   path('reg/', views.CustomUserAPIView.as_view(), name='registration_form'),
   path('log/', views.CustomLoginAPIView.as_view(), name='login_form'),
   path('change_password/', views.ChangePasswordAPIView.as_view(), name='change_password'),
   path('msg/', views.GetMessageAPIView.as_view(), name='message')
   # path('auth/', views.CustomLoginAPIView.as_view(), name = 'authentication_token')
]
