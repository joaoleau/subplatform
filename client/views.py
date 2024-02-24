from django.views.generic import TemplateView
from .mixins import NotIsactiveSubscriptionPermissionMixin


class SubscriptionLockedView(NotIsactiveSubscriptionPermissionMixin, TemplateView):
    template_name = "client/subscription-locked.html"
