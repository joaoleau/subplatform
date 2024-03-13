from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), max_length=100, unique=True)
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff"), default=False)
    is_superuser = models.BooleanField(_("superuser"), default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def is_sub(self) -> bool:
        sub = self.subscription
        plan, active = sub.get_plan_and_is_active()
        if active and plan.name != "Free":
            return True

        return False
