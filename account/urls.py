from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    LogoutView,
    AccountManagement,
    DeleteAccountView,
    EmailVerificationFailedView,
    EmailVerificationSentView,
    EmailVerificationSuccessView,
    EmailVerificationView,
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("account/management/", AccountManagement.as_view(), name="account-management"),
    path("delete/", DeleteAccountView.as_view(), name="account-delete"),
]

# Password urls
urlpatterns += [
    path(
        "reset_password",
        auth_views.PasswordResetView.as_view(
            template_name="account/password-reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password-reset-sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password-reset-form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
]

# Email urls
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
