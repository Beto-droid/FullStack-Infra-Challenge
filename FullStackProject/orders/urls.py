from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListCreateAPIView.as_view()),
    path('<int:pk>/', views.OrderDetailAPIView.as_view()),
    path('<int:pk>/update/', views.OrderUpdateAPIView.as_view()),
    path('<int:pk>/delete/', views.OrderDeleteAPIView.as_view()),
]