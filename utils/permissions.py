from django.utils import timezone

from rest_framework.permissions import BasePermission

from subscriptions.models import Subscription


class HasActiveSubscription(BasePermission):
    
    def has_permission(self,request,view):
        Subscription.objects.filter(
            user=request.user,
            expired_time__gt=timezone.now()
        ).exists()
            