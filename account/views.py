from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import TemplateView, FormView
from django.views import View
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy


class HomeView(TemplateView):
    template_name = "account/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(**kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


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
                return redirect("account:home")

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
