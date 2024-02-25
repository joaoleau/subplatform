from typing import Any
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .mixins import AuthorPermissionMixin
from .forms import ArticleForm
from .models import Article
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from client.mixins import SubscriptionPermissionMixin
from django.http import HttpRequest, HttpResponse


class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = "article/article-create.html"
    form_class = ArticleForm
    context_object_name = "form"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class MyArticlesView(LoginRequiredMixin, ListView):
    template_name = "article/my-articles.html"
    context_object_name = "article_list"
    model = Article

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "verbose_name": self.model._meta.verbose_name.title(),
                "verbose_name_plural": self.model._meta.verbose_name_plural.title(),
            }
        )
        return context

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class UpdateArticleView(AuthorPermissionMixin, UpdateView):
    template_name = "article/article-update.html"
    model = Article
    form_class = ArticleForm
    context_object_name = "article"
    pk_url_kwarg = "pk"


class DeleteArticleView(AuthorPermissionMixin, DeleteView):
    model = Article
    pk_url_kwarg = "pk"
    template_name = "article/article-confirm-delete.html"
    success_url = reverse_lazy("article:my-articles")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["article"] = self.get_object()
        return context


class DetailArticleView(LoginRequiredMixin, DetailView):
    template_name = "article/article-detail.html"
    model = Article
    context_object_name = "article"
    pk_url_kwarg = "pk"


class ListArticleView(SubscriptionPermissionMixin, ListView):
    template_name = "article/article-list.html"
    context_object_name = "article_list"
    model = Article

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "verbose_name": self.model._meta.verbose_name.title(),
                "verbose_name_plural": self.model._meta.verbose_name_plural.title(),
            }
        )
        return context

    def get_user_request(self):
        return get_user_model().objects.get(pk=self.request.user.id)

    def get_redirect_subscription_locked(self):
        return redirect("client:subscription-locked")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user = self.get_user_request()
        if not user.is_sub():
            return self.get_redirect_subscription_locked()
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any] | None:
        user = self.get_user_request()
        plan, is_active = user.subscription.get_plan_and_is_active()
        if is_active:
            if plan.name == "Standard":
                return self.model.objects.public_articles().standard()

            return self.model.objects.public_articles()

        return self.model.objects.none()
