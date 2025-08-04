from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import RegisterView, GetTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('get-token/', GetTokenView.as_view(), name='get-token'),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
