from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name"]


class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["email"]
