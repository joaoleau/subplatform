from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    LogoutView,
    AccountManagement,
    DeleteAccountView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("account/management/", AccountManagement.as_view(), name="account-management"),
    path("delete/", DeleteAccountView.as_view(), name="account-delete"),
]

urlpatterns += [
    path("reset/password/", PasswordResetView.as_view(), name="reset_password"),
    path(
        "reset/password/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/password/complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
