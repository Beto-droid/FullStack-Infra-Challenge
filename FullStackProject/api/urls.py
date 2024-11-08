from django.urls import path, include
from . import views


path('api-auth/', include('rest_framework.urls')),
# path('', views.api_home)
