from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListCreateAPIView.as_view()),  # Support filtering (?status) and pagination (?page=4&page_size=100)
    path('<uuid:id>/', views.OrderDetailAPIView.as_view()),
    path('<uuid:id>/update/', views.OrderRetrieveUpdateAPIView.as_view()),
    path('<uuid:id>/delete/', views.OrderRetrieveDeleteAPIView.as_view()),
]