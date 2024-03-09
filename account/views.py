from typing import Any
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.views.generic import FormView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import RegisterForm, LoginForm, UpdateUserForm
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail


User = get_user_model()


class LoginView(FormView):
    template_name = "account/login.html"
    form_class = LoginForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request, data=request.POST)

        if form.is_valid() and request.POST:
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                if not request.POST.get("remember_me", None):
                    request.session.set_expiry(0)
                login(request, user)

                return redirect("home")

        return self.render_to_response(
            self.get_context_data(error="Credenciais inválidas")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "account/register.html"
    success_url = reverse_lazy("email-verification-sent")
    success_message = "Novo usuário <b>%(username)s</b> criado com sucesso."

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("home")
        return self.render_to_response(self.get_context_data())

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            if password2 == password2:
                user.set_password(password1)
                user.is_active = False
                user.save()

                # Email verification
                current_site = get_current_site(request)
                subject = "Activate your account"
                message = render_to_string(
                    "account/email-verification.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": user_tokenizer_generate.make_token(user),
                    },
                )
                user_email = user.email
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,
                    recipient_list=[user_email],
                )

                return self.form_valid(form)
            else:
                form.add_error("password", "Senhas diferentes.")
                return self.form_invalid(form)

        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect("home")


class AccountManagement(LoginRequiredMixin, UpdateView):
    template_name = "account/update.html"
    model = User
    form_class = UpdateUserForm
    context_object_name = "form"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user"] = self.get_object()
        return context

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.get_queryset().get(pk=self.request.user.id)


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "account/account-confirm-delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.get_queryset().get(pk=self.request.user.id)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user"] = self.get_object()
        return context


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "account/password-reset.html"


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password-reset-sent.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password-reset-form.html"


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "account/password-reset-complete.html"


class EmailVerificationView(View):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        unique_token = force_str(urlsafe_base64_decode(self.kwargs["uidb64"]))
        user = User.objects.get(pk=unique_token)

        if user and user_tokenizer_generate.check_token(user, self.kwargs["token"]):
            user.is_active = True
            user.save()

            return redirect("email-verification-success")

        return redirect("email-verification-failed")


class EmailVerificationSentView(TemplateView):
    template_name = "account/email-verification-sent.html"


class EmailVerificationSuccessView(TemplateView):
    template_name = "account/email-verification-success.html"


class EmailVerificationFailedView(TemplateView):
    template_name = "account/email-verification-failed.html"
