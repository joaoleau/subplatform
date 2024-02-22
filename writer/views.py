from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import (
    ArticleForm,
)
from .models import Article


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "writer/writer-dashboard.html"


class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = "writer/create-article.html"
    form_class = ArticleForm
    context_object_name = "form"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)


class ListArticleView(LoginRequiredMixin, ListView):
    template_name = "writer/list-article.html"
    context_object_name = "article_list"
    model = Article

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            "verbose_name": self.model._meta.verbose_name.title(),
            "verbose_name_plural": self.model._meta.verbose_name_plural.title(),
        })
        return context


class DetailArticleView(LoginRequiredMixin, DetailView):
    template_name = "writer/article-detail.html"
    model = Article
    context_object_name = "article"
    pk_url_kwarg = 'pk'


class MyArticlesView(LoginRequiredMixin, ListView):
    template_name = "writer/my-articles.html"
    context_object_name = "article_list"
    model = Article

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            "verbose_name": self.model._meta.verbose_name.title(),
            "verbose_name_plural": self.model._meta.verbose_name_plural.title(),
        })
        return context

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

class UpdateArticleView(PermissionRequiredMixin, UpdateView):
    template_name = "writer/article-detail.html"
    model = Article
    context_object_name = "article"
    pk_url_kwarg = 'pk'
    permission_denied_message = "Permission denied"

    def has_permission(self) -> bool:
        return super().has_permission()