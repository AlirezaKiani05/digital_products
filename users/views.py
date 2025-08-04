import random
import uuid
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache
from django.shortcuts import render
from .models import User, Device,UserManager


class RegisterView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        
        
        if not phone_number:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            user=User.objects.get(phone_number=phone_number)
            return Response({'detail': 'User Already registered!'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user= User.objects.create_user(phone_number=phone_number)
           
        # user, created = User.objects.get_or_create(phone_number=phone_number)
        # if not created:
            # return Response({'detail': 'User Already registered!'}, status=status.HTTP_400_BAD_REQUEST)
        device = Device.objects.create(user=user)
        code = random.randint(10000, 99999)
        # send message(email or sms)
        # cache
        cache.set(str(phone_number), code, 2*60)

        return Response({'code': code})


class GetTokenView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        cached_code = cache.get(str(phone_number))
        if cached_code != code:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        token = str(uuid.uuid4())
        return Response({'token': token})
    
    

        
    
    
    
