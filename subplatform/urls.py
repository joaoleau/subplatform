from django.contrib import admin
from django.urls import path, include
from .views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("account.urls")),
    path("client/", include("client.urls")),
    path("", include("article.urls")),
    path("", HomeView.as_view(), name="home"),
]
