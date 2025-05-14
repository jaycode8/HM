from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("users", views.UserViewSet)

urlpatterns = [
    path("", views.index),
    path("login", views.sign_in, name="signin"),
    path("register", views.sign_up),
    path("dashboard", views.dashboard),
    path('logout', views.logout_view),
    path('enquiry', views.enquiry),
    path('sensors', views.sensors),
    path('auto-actions', views.automated_actions),
    path('data-logging', views.data_logging),
    path('tomato', views.tomato),
    path('detection', views.detection),
    path("api/", include(router.urls)),
]