from django.urls import path
from .views import (
    SubscriptionLockedView,
    SubscriptionPlansView,
    CreateSubscriptionView,
    DeleteSubscription,
    UpdateSubscription,
    PaypalUpdateSubConfirmed,
    DjangoUpdateSubConfirmed,
)

app_name = "client"

urlpatterns = [
    path(
        "subscription/locked/",
        SubscriptionLockedView.as_view(),
        name="subscription-locked",
    ),
    path(
        "subscription/plans/",
        SubscriptionPlansView.as_view(),
        name="subscription-plans",
    ),
    path(
        "subscription/create/<subID>/<plan>/",
        CreateSubscriptionView.as_view(),
        name="create-subscription",
    ),
    path(
        "subscription/delete/<subID>/",
        DeleteSubscription.as_view(),
        name="delete-subscription",
    ),
    path(
        "subscription/update/<subID>/",
        UpdateSubscription.as_view(),
        name="update-subscription",
    ),
    path(
        "subscription/update/confirmed",
        PaypalUpdateSubConfirmed.as_view(),
        name="update-subscription-confirmed",
    ),
    path(
        "subscription/update/confirmed/django/<subID>",
        DjangoUpdateSubConfirmed.as_view(),
        name="update-subscription-confirmed-django",
    ),
]
