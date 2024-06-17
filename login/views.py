from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

class SCViewLogin(LoginView):

    form_class = CustomAuthenticationForm
    template_name = 'sc_login.html'
