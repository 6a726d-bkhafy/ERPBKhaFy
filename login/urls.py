from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', SCViewLogin.as_view(), name = 'sc_login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
]