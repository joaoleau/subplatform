from django.urls import path
from .views import ListArticleView, SubscriptionLockedView

app_name = "client"

urlpatterns = [
    path("articles/", ListArticleView.as_view(), name="article-list"),
    path(
        "subscription-locked/",
        SubscriptionLockedView.as_view(),
        name="subscription-locked",
    ),
]
