from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):

    error_messages = {
        'invalid_login': 'Usuário ou senha incorretos'
    }