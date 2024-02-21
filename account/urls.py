from django.urls import path
from .views import (
    HomeView,
    LoginView,
    RegisterView,
    LogoutView
)

app_name = "account"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
