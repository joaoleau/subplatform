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
    
class DetailPermissionMixin(UserPassesTestMixin, LoginRequiredMixin):
    permission_denied_message = _("You don't have permission to see this article.")

    def test_func(self) -> bool:
        article = Article.objects.get(pk=self.kwargs["pk"])
        access = article.access_level
        user = self.request.user
        plan, active = user.subscription.get_plan_and_is_active()

        if  user == article.user:
            return True

        if (plan.name == "Free" or active == False) and (access in ["Premium", "Standard"]):
            return False

        if (user != article.user) and access == "Private":
            return False

        if user.is_sub():
            
            if (plan.name == "Standard" and access == "Premium"):
                return False
            
            return True
        
        return False

