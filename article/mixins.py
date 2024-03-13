from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Article
from django.utils.translation import gettext_lazy as _


class AuthorPermissionMixin(UserPassesTestMixin, LoginRequiredMixin):
    permission_denied_message = _("You don't have permission to edit this article.")

    def test_func(self) -> bool:
        article = Article.objects.get(pk=self.kwargs["pk"])
        return self.request.user == article.user


class AuthorOrSubscribePermissionMixin(UserPassesTestMixin, LoginRequiredMixin):
    permission_denied_message = _("You don't have permission to edit this article.")

    def test_func(self) -> bool:
        article = Article.objects.get(pk=self.kwargs["pk"])
        return (self.request.user == article.user) or (self.request.user.is_sub())
