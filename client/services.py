from .models import PlanModel
from django.contrib.auth import get_user_model
from .paypal import *


class ClientServices:
    model_user = get_user_model()

    def get_plan(self, plan: str) -> PlanModel:
        return PlanModel.objects.get(name=plan)
