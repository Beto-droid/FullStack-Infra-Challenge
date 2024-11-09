from django.urls import path
from .views import *

urlpatterns = [
    path('', order_list, name='front_end_main_view'),
]