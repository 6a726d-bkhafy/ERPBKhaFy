from django import template
from estoque.models import TBPROD

register = template.Library()

@register.filter
def cont(parameter):

    if parameter == 1:

        total = TBPROD.objects.filter(qtdestoque__gt = 0).count()

    else:

        total = TBPROD.objects.filter(qtdcsg__gt = 0).count()

    return total