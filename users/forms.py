from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = CustomUser.USER_TYPE_CHOICES
    USER_TYPE = forms.ChoiceField(choices=USER_TYPE_CHOICES, required = True, label='Sign up as')
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type')
        def clean_email(self):
            email= self.cleaned_data.get('email')
            if not re.match(r'^[\w.]+@[\w.]+\.[\w.]+$', email):
                raise forms.ValidationError('Enter a valid email address')
            return email
        def save(self, commit=True):
            user = super().save(commit=False)
            user.user_type = self.cleaned_data['user_type']
            if commit:
                user.save()
            return user

