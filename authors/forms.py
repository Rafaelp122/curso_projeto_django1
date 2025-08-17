from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. '
            'The length should be at least 8 characters.'
        )
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat you password',
        })
    )

    # Classe que utilizamos pra enviar metadados do nosso formulario
    # para o django
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]  # Aqui definimos os campos eu quero usar
        # exclude = ['first_name']

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

    def clean_password(self):
        # self.data: QueryDict com os dados brutos (strings) enviados pelo
        # usuário (ex.: request.POST)
        # self.cleaned_data: dict com valores validados e convertidos
        # (disponível após is_valid())
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(picoca)s no campo password',
                code='invalid',
                params={'pipoca': '"atenção"'}
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError({
                'password': 'Password and password2 must be equal',
                'password2': 'Password and password2 must be equal',
            })
