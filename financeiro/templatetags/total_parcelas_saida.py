from django import template
from financeiro.models import TBOFIN

register = template.Library()

@register.filter
def total(saida: TBOFIN):

    total = sum(i.dvlrtotal for i in TBOFIN.objects.filter(fk_tbcomp = saida.fk_tbcomp))

    return total