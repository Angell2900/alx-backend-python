from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_message, name='send_message'),
    path('messages/', views.get_messages, name='get_messages'),
    path('health/', views.health_check, name='health_check'),
]