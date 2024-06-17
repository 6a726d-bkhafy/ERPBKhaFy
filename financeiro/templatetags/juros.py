from django import template
from datetime import datetime
from cfg.models import CTBJURO
from decimal import Decimal

register = template.Library()

@register.filter
def calc(dtvenc, pend):

    dtdif = datetime.now() - dtvenc
    dif = Decimal(dtdif.days) if dtdif.days > 0 else 0

    try:
        obj_juro = CTBJURO.objects.latest('pk')
        juro = obj_juro.pvlr / 100
    except:
        juro = 0

    total = pend * (1 + juro) ** dif

    return round(total, 2)

@register.filter
def sub(valor1, valor2):

    return valor1 - valor2