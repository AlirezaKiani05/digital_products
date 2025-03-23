from django.urls import path

from .views import ProducListView,ProductDetailView


urlpatterns = [
    path('',ProducListView.as_view(),name='produc-list'),
    path('<int:pk>/',ProductDetailView.as_view(),name='product-detail'),
]