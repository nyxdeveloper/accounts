# django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = (
            "phone",
            "name",
            "password",
            "is_staff",
            "is_superuser",
            "is_active"
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "phone",
            "name",
            "password",
            "avatar",
            "is_staff",
            "is_superuser",
            "is_active"
        )
