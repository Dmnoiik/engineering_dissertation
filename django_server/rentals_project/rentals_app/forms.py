import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"id": "id_username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"id": "id_email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "id_password"}))

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]',
                                                                                                   password) or not re.search(
            r'[!@#$%^&*]', password):
            raise forms.ValidationError("Password must include uppercase, lowercase, number, and special character.")

        common_patterns = ["123", "qwerty", "haslozgaslo", "password", self.cleaned_data["username"].lower()]
        for pattern in common_patterns:
            if pattern in password.lower():
                raise forms.ValidationError("Password must not contain common patterns or personal information.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"id": "id_username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "id_password"}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("Nieprawidłowy login lub hasło")

        return cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user:
            # Log in the user using Django's authentication system
            if user.is_active:
                request.session.set_expiry(0)  # Session expiry (0 means session expires when the browser is closed)
                auth_login(request, user)
                return user

        return None
