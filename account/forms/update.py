from django import forms
from django.contrib.auth import get_user_model

class UpdateUserForm(forms.ModelForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "first_name",
            "last_name",
        ]
        exclude = ["password1", "password2"]