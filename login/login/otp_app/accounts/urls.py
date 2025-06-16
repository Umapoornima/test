from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('verify/', views.verify_otp, name='verify_otp'),
]
