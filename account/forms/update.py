from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

# class UpdateUserForm(forms.ModelForm):
#     password = None
#     class Meta:
#         model = User
#         fields = [
#             "email",
#             "first_name",
#             "last_name",
#         ]
#         exclude = ["password1", "password2"]


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
        ]
        exclude = ["password1", "password2"]