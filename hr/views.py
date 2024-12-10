import random
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.db import transaction
from rest_framework import  status
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from hrms.settings import EMAIL_HOST_USER
from rest_framework.authtoken.models import Token
from .models import *



@api_view(["POST"])
def token_login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"id":user.pk,"token": token.key,"role":[group.name for group in user.groups.all() ]}, status=status.HTTP_200_OK)
    return Response(
        {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(["GET"])
def get_all_users(request):
    try:
        users = User.objects.all()
        users_data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined,
                "is_active": user.is_active,
                "full_name":user.first_name,
                "role":[group.name for group in user.groups.all() ]
            }
            for user in users
        ]
        return JsonResponse({"users": users_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    
@api_view(["GET"])
def get_user_details(request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_joined": user.date_joined,
                "is_active": user.is_active,
                "groups": [group.name for group in user.groups.all()],
            }

            return JsonResponse(user_data, status=200)

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)