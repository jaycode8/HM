import jwt
from datetime import datetime, timedelta

from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer

# Create your views here.

@api_view(["GET"])
def logout_view(request):
    logout(request)

    response = redirect('/login')
    if 'auth_token' in request.COOKIES:
        response.delete_cookie('auth_token')

    return response

@api_view(["GET"])
def dashboard(request):
    token = request.COOKIES.get('auth_token')

    if not token and 'HTTP_AUTHORIZATION' in request.META:
        auth_header = request.META['HTTP_AUTHORIZATION']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

    if not token:
        return Response({"redirect": "/login"}, status=302, headers={"Location": "/login"})

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload['id']
        user = User.objects.get(id=user_id)
        user_data = UserSerializer(user).data

        return render(request, "dashboard/dashboard.html", {
            "user": user_data,
        })
    except jwt.ExpiredSignatureError:
        return Response({"redirect": "/login"}, status=302, headers={"Location": "/login"})
    except jwt.InvalidTokenError:
        return Response({"redirect": "/login"}, status=302, headers={"Location": "/login"})

# def dashboard(request):
#     return render(request, "dashboard/dashboard.html", {})

# @api_view(["GET"])
# def dashboard(request):
#     return render(request, "dashboard/dashboard.html", {})

@api_view(["GET"])
def index(request):
    return render(request, "index.html", {})

@api_view(["GET"])
def sign_up(request):
    return render(request, "auth/registration.html", {})

@api_view(["POST", "GET"])
def sign_in(request):
    if request.method == "POST":
        email = request.data.get('email')
        password = request.data.get('password')

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
        # return Response({
        #     "token": token,
        # }, status=200)

        response = Response({
            "token": token,
        }, status=200)

        response.set_cookie(
            key='auth_token',
            value=token,
            httponly=True,
            samesite='Lax',  # Prevents CSRF
            max_age=86400  # 1 day in seconds
        )

        return response

    else:
        return render(request, "auth/login.html", {})

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if request.data["password"] != request.data["confirm_password"]:
            raise ValidationError({'detail': "Passwords do not match."})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return redirect("/login")
