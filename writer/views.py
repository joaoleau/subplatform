from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .mixins import AuthorPermissionMixin, WriterPermissionMixin
from .forms import ArticleForm
from .models import Article


class DashboardView(WriterPermissionMixin, TemplateView):
    template_name = "writer/writer-dashboard.html"


class CreateArticleView(WriterPermissionMixin, CreateView):
    template_name = "writer/create-article.html"
    form_class = ArticleForm
    context_object_name = "form"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)


class MyArticlesView(WriterPermissionMixin, ListView):
    template_name = "writer/my-articles.html"
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
    template_name = "writer/update-article.html"
    model = Article
    form_class = ArticleForm
    context_object_name = "article"
    pk_url_kwarg = "pk"


class DeleteArticleView(AuthorPermissionMixin, DeleteView):
    model = Article
    pk_url_kwarg = "pk"
    template_name = "writer/article-confirm-delete.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["article"] = self.get_object()
        return context
    

class ListArticleView(WriterPermissionMixin, ListView):
    template_name = "writer/list-article.html"
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


class DetailArticleView(WriterPermissionMixin, DetailView):
    template_name = "writer/article-detail.html"
    model = Article
    context_object_name = "article"
    pk_url_kwarg = "pk"
