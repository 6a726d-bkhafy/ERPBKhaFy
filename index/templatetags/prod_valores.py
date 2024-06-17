from django import template
from financeiro.models import TBOPROD

register = template.Library()

@register.filter
def desc(prod: TBOPROD):

    return (prod.fk_tbprod.dvlrvenda - prod.dvlr) * prod.qtd

@register.filter
def total(prod: TBOPROD):

    return prod.dvlr * prod.qtd