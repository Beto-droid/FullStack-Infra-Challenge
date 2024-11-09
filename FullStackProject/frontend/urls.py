from django.urls import path
from .views import *

urlpatterns = [
    path('', order_list, name='front_end_main_view'),
    path('front/<uuid:id>/update/', update_order, name='update_order'),
    path('front/<uuid:id>/delete/', delete_order, name='delete_order'),
    path('front/create/', create_order, name='create_order'),
    path('front/<uuid:id>/edit', edit_order_row, name='edit_order_row'),
]