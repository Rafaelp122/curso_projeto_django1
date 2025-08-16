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
