from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='Контакты',
                                 help_text='Укажите номер телефона или '
                                     'имя в мессенджере (например telegram: @nick_name)',
                                 max_length=200)
    email = forms.EmailField(help_text='Почта потребуется, если Вы забудете пароль',
                             required=True,
                             max_length=200)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'password1',
                  'password2']


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Контакты',
                                 help_text='Укажите номер телефона или '
                                           'имя в мессенджере (например telegram: @nick_name)',
                                 max_length=200,
                                 required=False)
    email = forms.EmailField(help_text='Почта потребуется, если Вы забудете пароль',
                             required=True,
                             max_length=200)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name']
