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
    EmailVerificationFailedView,
    EmailVerificationSentView,
    EmailVerificationSuccessView,
    EmailVerificationView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("account/management/", AccountManagement.as_view(), name="account-management"),
    path("delete/", DeleteAccountView.as_view(), name="account-delete"),
]

#Password urls
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

#Email urls
urlpatterns += [
    path(
        "email/verification/<str:uidb64>/<str:token>/",
        EmailVerificationView.as_view(),
        name="email-verification",
    ),
    path(
        "email/verification/sent/",
        EmailVerificationSentView.as_view(),
        name="email-verification-sent",
    ),
    path(
        "email/verification/success/",
        EmailVerificationSuccessView.as_view(),
        name="email-verification-success",
    ),
    path(
        "email/verification/failed/",
        EmailVerificationFailedView.as_view(),
        name="email-verification-failed",
    ),
]
