from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


class PlanModel(models.Model):
    name = models.CharField(_("Plan Name"), max_length=20)
    cost = models.PositiveIntegerField(_("Cost"))

    def __str__(self) -> str:
        return f"{self.name}:{self.cost}"

    def get_plan_and_cost(self):
        return self.name


class Subscription(models.Model):
    plan = models.ForeignKey(
        PlanModel, on_delete=models.SET_NULL, null=True, related_name="subscriptions"
    )
    is_active = models.BooleanField(default=False)
    paypal_subscription_id = models.CharField(_("SubID"), max_length=300, default="XXX-XXX-XXX") #Implementar Default Para Free
    user = models.OneToOneField(
        User,
        max_length=10,
        on_delete=models.CASCADE,
        unique=True,
        related_name="subscription",
    )

    def get_subscriber_name(self) -> str:
        return self.user.full_name()

    def get_plan_and_is_active(self):
        if not User.objects.filter(pk=self.user.pk).exists():
            return None
        return self.plan, self.is_active

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.plan}"


@receiver(post_save, sender=User)
def create_default_subscription(sender, instance, created, **kwargs):
    if created:
        default_plan = PlanModel.objects.get(name="Free")
        Subscription.objects.create(plan=default_plan, user=instance, is_active=True)
