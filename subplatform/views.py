from typing import Any
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView


User = get_user_model()


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
