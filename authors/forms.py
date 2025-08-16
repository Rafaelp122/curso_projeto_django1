from django import forms
from django.contrib.auth.models import User


# Como já existe um model chamado User na base de dados, só de ter isso aqui já é possível de usar o formulario
class RegisterForm(forms.ModelForm):
    class Meta:  # Classe que utilizamos pra enviar metadados do nosso formulario para o django
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]  # Aqui definimos os campos eu quero usar

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password'
        }

        help_texts = {
            'email': 'The e-mail must be valid.'
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type you username here',
                'class': 'input text-input',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholver': 'Type your password here.'
            })
        }
