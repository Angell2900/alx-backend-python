
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # app routes first
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # DRF login/logout
]

