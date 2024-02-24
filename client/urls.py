from django.urls import path
from .views import SubscriptionLockedView

app_name = "client"

urlpatterns = [
    path(
        "subscription-locked/",
        SubscriptionLockedView.as_view(),
        name="subscription-locked",
    ),
]
