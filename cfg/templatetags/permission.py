from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def check(user: User, perm):

    return user.has_perm(perm)