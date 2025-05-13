from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, sign_in, sign_up, index, dashboard, logout_view

router = routers.DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("", index),
    path("login", sign_in, name="signin"),
    path("register", sign_up),
    path("dashboard", dashboard),
    path('logout', logout_view),
    path("api/", include(router.urls)),
]