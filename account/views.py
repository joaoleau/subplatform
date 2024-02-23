from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, FormView, UpdateView
from django.views import View
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy

User = get_user_model()

class HomeView(TemplateView):
    template_name = "account/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        if request.user.is_writer:
            return redirect("writer:writer-dashboard")
        else:
            return redirect("client:client-dashboard")


class LoginView(FormView):
    template_name = "account/login.html"
    form_class = LoginForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("account:home")
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
                if user.is_writer == True:
                    return redirect("writer:writer-dashboard")
                return redirect("client:client-dashboard")

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
    success_url = reverse_lazy("account:login")
    success_message = "Novo usuário <b>%(username)s</b> criado com sucesso."

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("account:home")
        return self.render_to_response(self.get_context_data())

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            if password2 == password2:
                user.set_password(password1)
                user.save()
                return self.form_valid(form)
            else:
                form.add_error("password", "Senhas diferentes.")
                return self.form_invalid(form)

        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("account:home")


class AccountManagement(UpdateView):
    template_name = "writer/article-detail.html"
    model = User
    context_object_name = "user"
    pk_url_kwarg = "pk"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.get_queryset().get(pk=self.request.user.id)
    