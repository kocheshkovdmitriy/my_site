from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AuthUser(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20, required=False, label='Имя пользователя')
    first_name = forms.CharField(max_length=20, required=False, label='Имя')
    last_name = forms.CharField(max_length=20, required=False, label='Фамилия')
    slug = forms.CharField(max_length=20, required=False, help_text='только латинские буквы и цифры')
    city = forms.CharField(required=False, label='Город')
    school = forms.CharField(required=False, label='Школа')
    grade = forms.IntegerField(required=False, label='Класс', help_text='Только число, без букв')
    slug.widget = slug.hidden_widget()

    def clean_username(self):
        name = self.cleaned_data['username']
        if not all([let.isdigit() or let in '-_' or ord('A') <= ord(let) <= ord('z') for let in name]):
            raise forms.ValidationError('Имя пользователя может содержать только латинские буквы, цифры - и _')
        return name

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)
