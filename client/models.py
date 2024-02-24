from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Subscription(models.Model):
    plan = models.CharField(_("Subscriber plan"), max_length=255)
    cost = models.CharField(_("Subscriber cost"), max_length=255)
    paypal_subscription_id = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)
    user = models.OneToOneField(
        get_user_model(),
        max_length=10,
        on_delete=models.CASCADE,
        unique=True,
        related_name="subscription",
    )

    def get_subscriber_name(self) -> str:
        return self.user.full_name()

    def get_plan_and_is_active(self):
        if not get_user_model().objects.filter(pk=self.user.pk).exists():
            return None
        return self.plan, self.is_active

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.plan} subscription"
