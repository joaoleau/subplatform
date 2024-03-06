from typing import Any
from django.http import HttpRequest
from django.shortcuts import redirect
from django.http.response import HttpResponse
from django.views.generic import TemplateView, View
from .mixins import NotIsactiveSubscriptionPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import PlanModel
from .paypal import *
from .services import ClientServices


class SubscriptionLockedView(NotIsactiveSubscriptionPermissionMixin, TemplateView):
    template_name = "client/subscription-locked.html"


class CreateSubscriptionView(LoginRequiredMixin, TemplateView):
    model_user = get_user_model()
    template_name = "client/create-subscription.html"
    services = ClientServices()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.user_object = self.request.user

        plan_name = self.kwargs.get("plan")

        self.user_object.subscription.plan = self.services.get_plan(plan_name)
        self.user_object.subscription.paypal_subscription_id = self.kwargs.get(
            "subID")
        self.user_object.subscription.save()

        return super().get(request, *args, **kwargs)


class DeleteSubscription(LoginRequiredMixin, TemplateView):
    access_token = get_access_token_paypal()
    template_name = "client/delete-subscription.html"
    services = ClientServices()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        subID = kwargs.get("subID")
        cancel_subscription_paypal(self.access_token, subID)

        user = self.request.user
        user.subscription.plan = self.services.get_plan("Free")
        user.subscription.save()

        return super().get(request, *args, **kwargs)


class SubscriptionPlansView(LoginRequiredMixin, TemplateView):
    template_name = "client/subscription-plans.html"
    model = PlanModel


class UpdateSubscription(LoginRequiredMixin, View):
    services = ClientServices()
    access_token = get_access_token_paypal()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        subID = kwargs.get("subID")

        approve_link = update_subscription_paypal(
            self.access_token, subID)

        if approve_link:
            return redirect(approve_link)

        else:
            return HttpResponse("Unable to obtain the approval link")


class PaypalUpdateSubConfirmed(LoginRequiredMixin, TemplateView):
    template_name = "client/paypal-update-sub-confirmed.html"
    extra_context = None

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        sub = self.request.user.subscription
        sub_id = sub.paypal_subscription_id
        self.extra_context = {"subID": sub_id}
        return super().get(request, *args, **kwargs)


class DjangoUpdateSubConfirmed(LoginRequiredMixin, TemplateView):
    template_name = "client/django-update-sub-confirmed.html"
    access_token = get_access_token_paypal()
    services = ClientServices()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        subID = kwargs.get("subID")
        self.user_object_with_subid = get_user_model().objects.get(
            subscription__paypal_subscription_id=subID)

        current_plan_id = get_current_subscription(self.access_token, subID)

        if current_plan_id == "P-79F92206JA736893VMXONXHI":
            new_plan = self.services.get_plan("Standard")
            self.user_object_with_subid.subscription.update(plan=new_plan)

        elif current_plan_id == "P-37W71531BU030260RMXN7HKY":
            new_plan = self.services.get_plan("Premium")
            self.user_object_with_subid.subscription.update(plan=new_plan)

        return super().get(request, *args, **kwargs)
