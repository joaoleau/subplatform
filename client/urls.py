from django.urls import path
from .views import DashboardView, ListArticleView, SubscriptionLockedView

app_name = "client"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="client-dashboard"),
    path("articles/", ListArticleView.as_view(), name="article-list"),
    path(
        "subscription-locked/",
        SubscriptionLockedView.as_view(),
        name="subscription-locked",
    ),
]
