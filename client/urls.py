from django.urls import path
from .views import DashboardView

app_name = "client"

urlpatterns = [path("dashboard/", DashboardView.as_view(), name="client-dashboard")]
