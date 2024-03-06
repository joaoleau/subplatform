from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UpdateUserForm(UserChangeForm):

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
        ]
        exclude = ["password1", "password2"]
