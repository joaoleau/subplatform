from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from writer.models import Article
from typing import Any
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from .mixins import NotIsactiveSubscriptionPermissionMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "client/client-dashboard.html"


class SubscriptionLockedView(NotIsactiveSubscriptionPermissionMixin, TemplateView):
    template_name = "client/subscription-locked.html"


class ListArticleView(LoginRequiredMixin, ListView):
    template_name = "client/list-article.html"
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
        if not user.get_subscription():
            return self.get_redirect_subscription_locked()
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any] | None:
        user = self.get_user_request()

        if user.get_subscription():
            plan, is_active = user.subscription.get_plan_and_is_active()

            if is_active is False:
                self.model.objects.none()

            elif plan == "Standard":
                return super().get_queryset().filter(is_premium=False)

            return super().get_queryset()

        return self.model.objects.none()
