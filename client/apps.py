from django.apps import AppConfig
from django.db.models.signals import post_migrate


def start_create_plans(sender, **kwargs):
    from .models import PlanModel

    if not PlanModel.objects.all().exists():
        PlanModel.objects.create(name="Free", cost=0)
        PlanModel.objects.create(name="Standard", cost=5)
        PlanModel.objects.create(name="Premium", cost=10)


class ClientConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "client"

    def ready(self) -> None:
        post_migrate.connect(start_create_plans, sender=self)
        return super().ready()
