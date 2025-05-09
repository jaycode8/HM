import jwt
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer

# Create your views here.

@api_view(["POST"])
def sign_in(request):
    data = JSONParser().parse(request)
    email = data['email']
    password = data['password']

    try:
        user = get_object_or_404(User, email=email)
    except:
        raise NotFound("Email does not exist")

    if not check_password(password, user.password):
        raise ValidationError({"detail": "Incorrect password"})

    token = jwt.encode(
        {"id": str(user.id), "exp": datetime.utcnow() + timedelta(days=1)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return Response({
        "token": token,
    }, status=200)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if request.data["password"] != request.data["confirm_password"]:
            raise ValidationError({'detail': "Passwords do not match."})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)