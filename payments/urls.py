from django.urls import path

from .views import PaymentView,GatewayView

urlpatterns = [
    path('gateways/',GatewayView.as_view(),name='gateways'),
    path('pay/',PaymentView.as_view(),name='payment'),
    
]
