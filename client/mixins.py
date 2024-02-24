from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext_lazy as _


class NotIsactiveSubscriptionPermissionMixin(UserPassesTestMixin, LoginRequiredMixin):
    permission_denied_message = _("Your account has been activated successfully.")

    def test_func(self) -> bool:
        return not self.request.user.get_subscription()


class SubscriptionPermissionMixin(UserPassesTestMixin, LoginRequiredMixin):
    permission_denied_message = _("Restricted access to subscribers.")

    def test_func(self) -> bool:
        return self.request.user.get_subscription()
