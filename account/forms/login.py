from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from ..models import User

class LoginForm(AuthenticationForm):
    pass
