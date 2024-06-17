from cfg.models import CTBCATFIN, CTBBANK, CTBEMP
from .models import *
from datetime import datetime
from decimal import Decimal
import calendar
from estoque.models import TBCSG, STBOCSG, TBIOCSG
from django.db.models.query import QuerySet, Q
from django.db.models import F, Min
from index.pdf_creator.create_table_fpdf2 import PDF
import os
from django.conf import settings
from django.template.loader import get_template
import urllib.parse
import subprocess
import json

def gerar_lancamento_convencional(request):

    numnota = request.POST.get('dado_numnota')
    fornecedor = TBFORN.objects.get(pk = request.POST.get('id_fornecedor'))
    valor = request.POST.get('dado_valor')
    custo = CTBCATFIN.objects.get(pk = request.POST.get('id_custo'))
    emissao = request.POST.get('dado_emissao')
    venc = request.POST.get('dado_venc')
    dsc = request.POST.get('dado_dsc')

    if 'dado_boleto' in request.FILES:

        boleto = request.FILES['dado_boleto']

        try:
            ultimo_fin = TBOFIN.objects.latest('pk')
            boleto.name = f'{ultimo_fin.pk + 1}_{fornecedor.pk}_{numnota}.png'
            
        except TBOFIN.DoesNotExist:
            boleto.name = f'1_{fornecedor.pk}_{numnota}.png'
    
    else:
        boleto = None

    fin = TBOFIN(
        numnota = numnota,
        fk_tbforn = fornecedor,
        dvlrtotal = valor,
        dvlrpend = valor,
        fk_ctbcatfin = custo,
        dtem = emissao,
        dtvenc = venc,
        dsc = dsc,
        comprod = False,
        boleto = boleto,
        tipoop = '5',
        sts = '0'
    )

    fin.save()

def realizar_pagamento(request):

    saida = TBOFIN.objects.get(pk = request.POST.get('id_saida'))
    tipopg = request.POST.get('dado_pg')
    valor = Decimal(request.POST.get('dado_valor'))
    caixa = TBIOCX.objects.latest('pk')

    try:
        conta = CTBBANK.objects.get(pk = request.POST.get('id_conta'))
    except:
        conta = None

    if tipopg == '5':
        caixa.dvlr -= valor
        caixa.save()

    pg = TBOPG(
        fk_tbofin = saida,
        dtpg = datetime.now(),
        dvlr = valor,
        fk_ctbbank = conta,
        tipopg = tipopg,
        sts = '0',
        fk_tbiocx = caixa if tipopg == '5' else None
    )
    pg.save()

    saida.dvlrpend -= valor

    if saida.dvlrpend == 0:
        saida.sts = '1'
    else:
        saida.sts = '2'

    saida.save()

def realizar_pagamento_entrada_dinheiro(request):

    entrada = TBIFIN.objects.get(pk = request.POST.get('id_entrada'))
    valor = Decimal(request.POST.get('dado_valor_pago'))
    caixa = TBIOCX.objects.latest('pk')
    juro = request.POST.get('dado_juro')
    
    troco = valor - entrada.dvlrpend if valor > entrada.dvlrpend else 0
    valor -= troco

    caixa.dvlr += valor
    caixa.save()

    pg = TBIPG(
        fk_tbifin = entrada,
        dtpg = datetime.now(),
        dvlr = valor,
        sts = '0',
        fk_tbiocx = caixa,
        fk_tbcx = entrada.fk_tbicred.fk_tbcx,
        dif = juro
    )
    pg.save()

    cliente = entrada.fk_tbcli
    cliente.creddisp += valor
    cliente.save()

    entrada.dvlrpend -= valor

    if entrada.dvlrpend == 0:
        entrada.sts = '1'
        cred = entrada.fk_tbicred
        cred.qtdpaga += 1
        try:
            prox_parcela = TBIFIN.objects.filter(fk_tbicred = cred, sts = '4').annotate(menor_data = Min('dtvenc')).filter(dtvenc = F('menor_data')).first()
            prox_parcela.sts = '0'
            prox_parcela.save()
        except:
            pass
        cred.save()
    else:
        entrada.sts = '2'

    entrada.save()

def realizar_pagamento_entrada_outros(request):

    entrada = TBIFIN.objects.get(pk = request.POST.get('id_entrada'))
    valor = Decimal(request.POST.get('dado_valor_pago'))
    valortotal = Decimal(request.POST.get('dado_total'))
    tipopg = CTBITIPOPG.objects.get(pk = request.POST.get('dado_tipopg'))
    juro = request.POST.get('dado_juro')

    if valor > valortotal:
        error_dict = {'dado_valor_pago': ['Valor pago acima do devido!']}
        raise ValidationError(error_dict)

    pg = TBIPG(
        fk_tbifin = entrada,
        dtpg = datetime.now(),
        dvlr = valor,
        sts = '0',
        fk_ctbitipopg = tipopg,
        fk_ctbbank = tipopg.fk_ctbbank,
        fk_tbcx = entrada.fk_tbicred.fk_tbcx,
        dif = juro
    )
    pg.save()

    cliente = entrada.fk_tbcli
    cliente.creddisp += valor
    cliente.save()

    entrada.dvlrpend -= valor

    if entrada.dvlrpend == 0:
        entrada.sts = '1'
        cred = entrada.fk_tbicred
        cred.qtdpaga += 1
        try:
            prox_parcela = TBIFIN.objects.filter(fk_tbicred = cred, sts = '4').annotate(menor_data = Min('dtvenc')).filter(dtvenc = F('menor_data')).first()
            prox_parcela.sts = '0'
            prox_parcela.save()
        except:
            pass
        cred.save()
    else:
        entrada.sts = '2'

    entrada.save()

def definir_tabela(request):

    if request.POST.get('id_venda_pdv'):
        vendas = STBOPROD.objects.filter(fk_user = request.user)

    if request.POST.get('id_venda_consignado'):
        vendas = STBOCSG.objects.filter(fk_tbcsg__pk = request.POST.get('id_venda_consignado'), sel = True)

    if request.POST.get('id_venda_troca'):
        vendas = STBOTPROD.objects.filter(fk_tbtprod__pk = request.POST.get('id_venda_troca'))

    return vendas

def validar_estoque(request, vendas: QuerySet[STBOPROD]):

    produto = TBPROD.objects.get(pk = request.POST.get('id_produto'))
    vendas.filter(fk_tbprod = produto, estoque = True)

    if vendas:

        if vendas[0].qtd < produto.qtdestoque:

            return True
        
        else:

            return False

    elif produto.qtdestoque > 0:

        return True
    
    else:

        return False

def adicionar_produto_a_lista(request, estoque, vendas: QuerySet[STBOPROD]):

    produto = TBPROD.objects.get(pk = request.POST.get('id_produto'))
    venda = vendas.filter(fk_tbprod = produto, estoque = estoque)
    if request.POST.get('id_venda_consignado'):
        venda = venda.filter(sts = '1')

    if venda:

        venda[0].qtd += 1
        total = venda[0].dvlrtotal + produto.dvlrvenda * (1 - (venda[0].pvlrdesc / 100))
        venda[0].dvlrtotal = round(total, 2)
        venda[0].save()
    
    elif request.POST.get('id_venda_pdv'):

        venda = STBOPROD(
            fk_tbprod = produto,
            qtd = 1,
            dvlrtotal = produto.dvlrvenda,
            pvlrdesc = 0,
            fk_user = request.user,
            estoque = estoque,
            dvlrund = produto.dvlrvenda
        )
        venda.save()

    elif request.POST.get('id_venda_consignado'):

        venda = STBOCSG(
            fk_tbprod = produto,
            qtd = 1,
            dvlrtotal = produto.dvlrvenda,
            pvlrdesc = 0,
            fk_tbcsg = TBCSG.objects.get(pk = request.POST.get('id_venda_consignado')),
            estoque = estoque,
            dvlrund = produto.dvlrvenda,
            sts = '1'
        )
        venda.save()
    
    elif request.POST.get('id_venda_troca'):

        venda = STBOTPROD(
            fk_tbprod = produto,
            qtd = 1,
            dvlrtotal = produto.dvlrvenda,
            pvlrdesc = 0,
            fk_tbtprod = TBTPROD.objects.get(pk = request.POST.get('id_venda_troca')),
            estoque = estoque,
            dvlrund = produto.dvlrvenda
        )
        venda.save()

def remover_produto_da_lista(request, vendas: QuerySet[STBOPROD]):

    venda = vendas.get(pk = request.POST.get('id_venda'))
    venda.delete()

def remover_todos_os_produtos_da_lista(request, vendas: QuerySet[STBOPROD]):

    if request.POST.get('id_venda_consignado'):
        vendas = vendas.filter(sts = '1')
        STBOCSG.objects.filter(fk_tbcsg__pk = request.POST.get('id_venda_consignado')).update(sel = True)

    vendas.delete()

def fechar_caixa():

    caixa = TBIOCX.objects.latest('pk')
    caixa.sts = 0
    caixa.save()

def abrir_caixa():

    try:
        caixa = TBIOCX.objects.latest('pk')
    except TBIOCX.DoesNotExist:
        caixa = None

    new_caixa = TBIOCX(
        dvlr = caixa.dvlr if caixa is not None else 0,
        sts = 1
    )
    new_caixa.save()

def realizar_sangria(request):

    valor = Decimal(request.POST.get('dado_valor'))

    caixa = TBIOCX.objects.latest('pk')
    caixa.dvlr -= valor
    caixa.save()

    entrada_fin = TBIFIN(
        dvlrtotal = valor,
        dvlrpend = 0,
        dtem = datetime.now(),
        dtvenc = datetime.now().date(),
        sts = '1',
        tipoop = 4,
    )
    entrada_fin.save()

def aplicar_desconto(request, vendas: QuerySet[STBOPROD]):

    venda = vendas.get(pk = request.POST.get('id_venda'))
    desconto = Decimal(request.POST.get('dado_desconto'))

    valor_total = venda.fk_tbprod.dvlrvenda * venda.qtd

    venda.pvlrdesc = desconto
    venda.dvlrtotal = valor_total - (valor_total * desconto / 100)
    venda.dvlrund = venda.fk_tbprod.dvlrvenda - (venda.fk_tbprod.dvlrvenda * desconto / 100)

    venda.save()

def aplicar_quantidade(request, vendas: QuerySet[STBOPROD]):

    venda = vendas.get(pk = request.POST.get('id_venda'))
    quantidade = Decimal(request.POST.get('dado_qtd'))
    
    venda.qtd = quantidade
    valor_total = venda.fk_tbprod.dvlrvenda * venda.qtd
    venda.dvlrtotal = valor_total

    venda.save()


def nova_movimentacao_de_caixa(request, tipopg = None, qtdparc = 1):

    usuario = User.objects.get(pk = request.POST.get('id_usuario'))
    cliente = TBCLI.objects.get(pk = request.POST.get('id_cliente'))
    total = Decimal(request.POST.get('dado_total'))

    if request.POST.get('dado_desconto_dinheiro'):
        desconto = Decimal(request.POST.get('dado_desconto_dinheiro'))
    elif request.POST.get('dado_desconto_cartao'):
        desconto = Decimal(request.POST.get('dado_desconto_cartao'))
    else:
        desconto = 0

    caixa = TBCX(
        dvlr = total - desconto,
        fk_user = usuario,
        fk_tbcli = cliente,
        dt = datetime.now(),
        sts = '0',
        fk_ctbitipopg = tipopg,
        qtdparc = qtdparc
    )
    caixa.save()

    return caixa, desconto

def nova_movimentacao_de_caixa_cred(request, tipopg = None, qtdparc = 1):

    usuario = User.objects.get(pk = request.POST.get('id_usuario'))
    cliente = TBCLI.objects.get(pk = request.POST.get('id_cliente'))
    total = Decimal(request.POST.get('dado_total'))

    if request.POST.get('dado_desconto_dinheiro'):
        desconto = Decimal(request.POST.get('dado_desconto_dinheiro'))
    elif request.POST.get('dado_desconto_cartao'):
        desconto = Decimal(request.POST.get('dado_desconto_cartao'))
    else:
        desconto = 0

    dtven = request.POST.get('dado_data_venda')
    dtven = datetime.strptime(dtven, "%Y-%m-%d")

    caixa = TBCX(
        dvlr = total - desconto,
        fk_user = usuario,
        fk_tbcli = cliente,
        dt = dtven,
        sts = '0',
        crediario = '1',
        fk_ctbitipopg = tipopg,
        qtdparc = qtdparc
    )
    caixa.save()

    return caixa, desconto

def nova_saida_de_produtos(caixa: TBCX, desconto, vendas: QuerySet[STBOPROD]):

    saidas = []

    for venda in vendas:

        new_valor = (venda.dvlrtotal - (desconto * (venda.dvlrtotal / (caixa.dvlr + desconto)))) / venda.qtd

        saida = TBOPROD(
            fk_tbprod = venda.fk_tbprod,
            dvlr = round(new_valor, 2),
            qtd = venda.qtd,
            fk_tbcx = caixa,
            tipomov = '5',
            sts = '0' if venda.estoque == True else '5'
        )
        saidas.append(saida)

    TBOPROD.objects.bulk_create(saidas)

def novo_lancamento_financeiro(caixa: TBCX):

    try:
        ultima_entrada = TBIFIN.objects.latest('numnota')
        numnota = ultima_entrada.numnota + 1
    except:
        numnota = 1

    entrada_fin = TBIFIN(
        fk_tbcli = caixa.fk_tbcli,
        dvlrtotal = caixa.dvlr,
        dvlrpend = caixa.dvlr,
        dtem = datetime.now(),
        dtvenc = datetime.now().date(),
        sts = '1',
        tipoop = '4',
        numnota = numnota,
        fk_tbcx = caixa
    )
    entrada_fin.save()

    return entrada_fin

def novo_pagamento(desconto, caixa: TBCX, entrada_fin = None):

    pg = TBIPG(
        fk_tbifin = entrada_fin,
        dtpg = datetime.now(),
        dvlr = caixa.dvlr + desconto,
        fk_ctbitipopg = caixa.fk_ctbitipopg,
        sts = '0',
        fk_tbiocx = TBIOCX.objects.latest('pk') if not caixa.fk_ctbitipopg else None,
        fk_tbcx = caixa,
        dif = 0 - desconto
    )
    pg.save()

def novo_lancamento_financeiro_crediario(request, caixa: TBCX):

    try:
        ultima_entrada = TBIFIN.objects.latest('numnota')
        numnota = ultima_entrada.numnota + 1
    except:
        numnota = 1

    cliente = caixa.fk_tbcli
    cliente.creddisp -= caixa.dvlr
    cliente.save()

    cred = TBICRED(
        qtdparc = caixa.qtdparc,
        qtdpaga = 0,
        dvlr = caixa.dvlr,
        fk_tbcx = caixa
    )
    cred.save()

    dt = request.POST.get('dado_data')
    dt = datetime.strptime(dt, "%Y-%m-%d")

    dtven = request.POST.get('dado_data_venda')
    dtven = datetime.strptime(dtven, "%Y-%m-%d")

    parcela = caixa.dvlr / caixa.qtdparc

    entradas = []

    for i in range(caixa.qtdparc):

        entrada_fin = TBIFIN(
            fk_tbcli = caixa.fk_tbcli,
            dvlrtotal = parcela,
            dvlrpend = parcela,
            dtem = dtven,
            dtvenc = dt,
            sts = '0' if i == 0 else '4',
            tipoop = '4',
            numnota = numnota,
            fk_tbicred = cred,
            fk_tbcx = caixa
        )
        entradas.append(entrada_fin)

        ano = dt.year
        mes = dt.month + 1
        if mes > 12:
            mes = 1
            ano += 1

        ultimo_dia_do_mes = calendar.monthrange(ano, mes)[1]
        dia = min(dt.day, ultimo_dia_do_mes)

        dt = datetime(ano, mes, dia)
    
    TBIFIN.objects.bulk_create(entradas)
    
def ajustar_estoque(request, vendas: QuerySet[STBOPROD]):

    if request.POST.get('id_venda_consignado'):

        for venda in vendas:

            if venda.estoque == True and venda.sts == '1':

                produto = venda.fk_tbprod
                produto.qtdestoque -= venda.qtd
                produto.save()

            if venda.sts == '0':

                produto = venda.fk_tbprod
                produto.qtdcsg -= venda.qtd
                produto.save()

    else:

        for venda in vendas:

            if venda.estoque == True:

                produto = venda.fk_tbprod
                produto.qtdestoque -= venda.qtd
                produto.save()

def ajustar_caixa(request):

    total = Decimal(request.POST.get('dado_total'))
    caixa = TBIOCX.objects.latest('pk')

    caixa.dvlr += total
    caixa.save()

def novo_consignado(request, vendas: QuerySet[STBOPROD]):

    cliente = TBCLI.objects.get(pk = request.POST.get('id_cliente'))
    usuario = User.objects.get(pk = request.POST.get('id_usuario'))
    dtfim = request.POST.get('dado_data')
    total = Decimal(request.POST.get('dado_total'))
    
    qtd = sum(i.qtd for i in vendas)

    consignado = TBCSG(
        fk_tbcli = cliente,
        fk_user = usuario,
        qtd = qtd,
        dtinicio = datetime.now(),
        dtfim = dtfim,
        sts = '0',
        dvlr = total
    )
    consignado.save()

    cliente.consdisp -= total
    cliente.save()

    return consignado

def inserir_produtos_em_consignado(consignado, vendas: QuerySet[STBOPROD]):

    lista_cons = []
    lista_cons_venda = []

    for venda in vendas:

        cons = TBIOCSG(
            fk_tbprod = venda.fk_tbprod,
            qtd = venda.qtd,
            fk_tbcsg = consignado,
            sts = '0',
            estoque = venda.estoque
        )
        lista_cons.append(cons)

        cons_venda = STBOCSG(
            qtdtotal = venda.qtd,
            qtd = venda.qtd,
            dvlrtotal = venda.fk_tbprod.dvlrvenda * venda.qtd,
            dvlrund = venda.dvlrund,
            fk_tbprod = venda.fk_tbprod,
            fk_tbcsg = consignado,
            estoque = venda.estoque,
            sts = '0'
        )
        lista_cons_venda.append(cons_venda)

    STBOCSG.objects.bulk_create(lista_cons_venda)
    TBIOCSG.objects.bulk_create(lista_cons)

def ajustar_estoque_consignado(vendas: QuerySet[STBOPROD]):

    for venda in vendas:

        produto = venda.fk_tbprod
        produto.qtdestoque -= venda.qtd if venda.estoque == True else 0
        produto.qtdcsg += venda.qtd
        produto.save()

def remover_consignado_da_lista(request, vendas: QuerySet[STBOCSG]):

    venda = vendas.get(pk = request.POST.get('id_venda'))
    venda.sel = False
    venda.qtd = venda.qtdtotal
    venda.save()

def alterar_quantidade_consignado(request, vendas: QuerySet[STBOCSG]):

    venda = vendas.get(pk = request.POST.get('id_venda'))
    qtd = int(request.POST.get('dado_qtd'))

    valor_total = venda.fk_tbprod.dvlrvenda * qtd

    venda.qtd = qtd
    venda.dvlrtotal = valor_total - (valor_total * venda.pvlrdesc / 100)
    venda.save()

def fechar_consignado(request, vendas: QuerySet[STBOCSG]):

    cons = TBIOCSG.objects.filter(fk_tbcsg__pk = request.POST.get('id_venda_consignado'))
    consignado = TBCSG.objects.get(pk = request.POST.get('id_venda_consignado'))
    vendas = vendas.filter(sts = '0')

    cliente = consignado.fk_tbcli
    
    for venda in vendas:

        cliente.consdisp += venda.dvlrtotal
        cliente.save()

        prod_consignado = cons.filter(fk_tbprod = venda.fk_tbprod, sts = '0')
        prod_venda = cons.filter(fk_tbprod = venda.fk_tbprod, sts = '3')

        if prod_consignado:

            prod_consignado[0].qtd -= venda.qtd
            prod_consignado[0].save() if prod_consignado[0].qtd > 0 else prod_consignado[0].delete()

        if prod_venda:

            prod_venda[0].qtd += venda.qtd
            prod_venda[0].save()

        else:

            new_cons = TBIOCSG(
                fk_tbprod = venda.fk_tbprod,
                fk_tbcsg = consignado,
                qtd = venda.qtd,
                sts = '3',
                estoque = venda.estoque
            )
            new_cons.save()

        venda.qtdtotal -= venda.qtd
        venda.qtd = venda.qtdtotal
        venda.save()

        if venda.qtdtotal == 0:
            venda.delete()

    total_em_consignado = sum(i.qtd for i in cons.filter(sts = '0'))

    if total_em_consignado == 0:

        consignado.sts = '2'
    
    elif total_em_consignado < consignado.qtd:

        consignado.sts = '1'

    consignado.save()

def criar_ordem_de_troca(request):

    caixa = TBCX.objects.get(pk = request.POST.get('id_caixa'))
    prod_caixa = TBOPROD.objects.filter(Q(fk_tbcx = caixa) & ~Q(sts = '1') & ~Q(sts = '2'))

    qtd = 0
    valor = 0

    for prod in prod_caixa:

        qtd = int(request.POST.get(f'dado_{prod.fk_tbprod}_{prod.pk}')) if request.POST.get(f'dado_{prod.fk_tbprod}_{prod.pk}') else 0
        valor += prod.dvlr * qtd

        print(valor)

    print(valor)

    troca = TBTPROD(
        fk_tbcx_entrada = caixa,
        fk_tbcli = caixa.fk_tbcli,
        dvlr = valor,
        sts = '0',
        dt = datetime.now()
    )
    troca.save()

    list_new_prod = []
    list_troca_prod = []

    for prod in prod_caixa:

        qtd = int(request.POST.get(f'dado_{prod.fk_tbprod}_{prod.pk}')) if request.POST.get(f'dado_{prod.fk_tbprod}_{prod.pk}') else 0

        if qtd != 0:
            prod.qtd -= qtd
            prod.save() if prod.qtd != 0 else prod.delete()

            new_prod = TBOPROD(
                fk_tbprod = prod.fk_tbprod,
                qtd = qtd,
                fk_tbcx = prod.fk_tbcx,
                tipomov = prod.tipomov,
                sts = '2',
                dvlr = prod.dvlr,
                fk_tbtprod = troca
            )
            list_new_prod.append(new_prod)

            troca_prod = TBIOTPROD(
                fk_tbtprod = troca,
                fk_tbprod = prod.fk_tbprod,
                dvlr = prod.dvlr,
                qtd = qtd,
                sts = '0'
            )
            list_troca_prod.append(troca_prod)

    total_disponivel_para_troca = sum(i.qtd for i in prod_caixa if i.sts == '0' or i.sts == '5')
    if total_disponivel_para_troca == 0:
        caixa.sts = '2'
        caixa.save()

    TBOPROD.objects.bulk_create(list_new_prod)
    TBIOTPROD.objects.bulk_create(list_troca_prod)

def fechar_troca(request, caixa, vendas: QuerySet[STBOTPROD]):

    troca = TBTPROD.objects.get(pk = request.POST.get('id_venda_troca'))
    TBIOTPROD.objects.filter(fk_tbtprod = troca).update(sts = '2')
    TBOPROD.objects.filter(fk_tbtprod = troca).update(sts = '1')

    prod_caixa = TBOPROD.objects.filter(fk_tbcx = troca.fk_tbcx_entrada)
    qtd_vend = sum(prod.qtd for prod in prod_caixa if prod.sts != '1' and prod.sts != '2')

    if qtd_vend == 0:

        caixa_entrada = troca.fk_tbcx_entrada
        caixa_entrada.sts = '1'
        caixa_entrada.save()

    troca.sts = '1'
    troca.fk_tbcx_saida = caixa
    troca.save()

    list_prod_troca = []

    for venda in vendas:

        prod_troca = TBIOTPROD(
            fk_tbtprod = troca,
            fk_tbprod = venda.fk_tbprod,
            dvlr = venda.dvlrund,
            qtd = venda.qtd,
            sts = '3'
        )
        list_prod_troca.append(prod_troca)

    TBIOTPROD.objects.bulk_create(list_prod_troca)

def realizar_estorno_de_pagamento_entrada(pg: TBIPG):

    pg.sts = '1'
    pg.save()

    if not pg.fk_ctbitipopg:

        caixa = pg.fk_tbiocx
        caixa.dvlr -= pg.dvlr
        caixa.save()

    if pg.fk_tbifin:

        if pg.fk_tbifin.fk_tbicred and pg.fk_tbifin.sts == '1':

            cred = pg.fk_tbifin.fk_tbicred
            cred.qtdpaga -= 1
            cred.save()
            cliente = pg.fk_tbifin.fk_tbcli
            cliente.creddisp -= pg.dvlr
            cliente.save()
        
        fin = pg.fk_tbifin
        fin.dvlrpend += pg.dvlr
        fin_pgs = TBIPG.objects.filter(fk_tbifin = fin, sts = '0')
        if fin_pgs:
            fin.sts = '2'
        else:
            fin.sts = '0'
        fin.save()

def realizar_estorno_de_pagamento_saida(pg: TBOPG):

    pg.sts = '1'
    pg.save()

    if pg.tipopg == '5':

        caixa = pg.fk_tbiocx
        caixa.dvlr += pg.dvlr
        caixa.save()

    if pg.fk_tbofin:
        
        fin = pg.fk_tbofin
        fin.dvlrpend += pg.dvlr
        fin_pgs = TBOPG.objects.filter(fk_tbofin = fin, sts = '0')
        if fin_pgs:
            fin.sts = '2'
        else:
            fin.sts = '0'
        fin.save()

def realizar_estorno_de_caixa(request):

    caixa = TBCX.objects.get(pk = request.POST.get('id_caixa'))

    if not caixa.fk_ctbitipopg and caixa.crediario == 1:

        cliente = caixa.fk_tbcli
        cliente.creddisp += caixa.dvlr
        cliente.save()
    
    if not caixa.fk_ctbitipopg and not caixa.crediario and caixa.qtdparc == 1:

        pg = TBIPG.objects.filter(fk_tbcx = caixa)
        cx = pg[0].fk_tbiocx
        cx.dvlr -= caixa.dvlr
        cx.save()
        pg.update(sts = '1')

    if not caixa.fk_ctbitipopg and caixa.qtdparc > 1:

        cliente = caixa.fk_tbcli
        cliente.creddisp += caixa.dvlr
        cliente.save()

    caixa.sts = '4'
    caixa.save()
    TBOPROD.objects.filter(fk_tbcx = caixa).update(sts = '4')
    TBIFIN.objects.filter(fk_tbcx = caixa).update(sts = '3')
    TBIPG.objects.filter(fk_tbcx = caixa).update(sts = '1')

def alterar_data_de_vencimento_saida(request):

    dtvenc = request.POST.get('dado_dtvenc')
    fin = TBOFIN.objects.get(pk = request.POST.get('id_saida'))

    fin.dtvenc = dtvenc
    fin.save()

def alterar_valor_das_parcelas_saida(request):

    saida = TBOFIN.objects.get(pk = request.POST.get('id_saida'))

    error = ''

    saidas = TBOFIN.objects.filter(fk_tbcomp = saida.fk_tbcomp)

    list_valor = []

    for saida in saidas:

        if saida.sts == '0':
            valor = Decimal(request.POST.get(f'dado_{saida.pk}'))
        else:
            valor = saida.dvlrtotal
        list_valor.append(valor)

    total = sum(i for i in list_valor)

    if total != Decimal(request.POST.get('dado_total')):

        error = f'A soma de todas as parcelas deve corresponder a R$ {request.POST.get("dado_total")}, porém resulta em R$ {total}!'

    else:

        for saida in saidas.filter(sts = '0'):

            valor = Decimal(request.POST.get(f'dado_{saida.pk}'))
            saida.dvlrtotal = valor
            saida.dvlrpend = valor
            saida.save()

    return error

def alterar_data_de_vencimento_entrada(request):

    dtvenc = request.POST.get('dado_dtvenc')
    fin = TBIFIN.objects.get(pk = request.POST.get('id_entrada'))

    fin.dtvenc = dtvenc
    fin.save()

def alterar_valor_das_parcelas(request):

    cred = TBICRED.objects.get(pk = request.POST.get('id_crediario'))
    entradas = TBIFIN.objects.filter(fk_tbicred = cred)

    list_valor = []

    for ent in entradas:

        valor = Decimal(request.POST.get(f'dado_{ent.pk}'))
        list_valor.append(valor)

    total = sum(i for i in list_valor)

    cred.dvlr = total
    cred.save()

    for ent in entradas:

        valor = Decimal(request.POST.get(f'dado_{ent.pk}'))
        ent.dvlrtotal = valor
        ent.dvlrpend = valor
        ent.save()

def nova_transferencia(request):

    conta_in = CTBBANK.objects.get(pk = request.POST.get('id_conta_in'))
    conta_out = CTBBANK.objects.get(pk = request.POST.get('id_conta_out'))
    total = request.POST.get('dado_total')

    transf = TBIOTRANSF(
        fk_ctbbank_in = conta_in,
        fk_ctbbank_out = conta_out,
        dvlr = total,
        dt = datetime.now(),
        fk_user = request.user
    )
    transf.save()

def estornar_lancamento(request):

    saida = TBOFIN.objects.get(pk = request.POST.get('id_saida'))

    saida.sts = '3'
    saida.save()

def gerar_nf_venda(request, caixa: TBCX, desconto, tipopg):

    valorpago = request.POST.get('dado_valor_pago')

    date = datetime.now()
    dt = str(date.date()).split('-')
    dt = f'{dt[2]}/{dt[1]}/{dt[0]}'
    hour = f'{date.hour}:{date.minute}'

    emp = CTBEMP.objects.latest('pk')

    entradas = TBIFIN.objects.filter(fk_tbcx = caixa)

    vendas = TBOPROD.objects.filter(fk_tbcx = caixa)

    context = {
        'tipolayout': 1,
        'dt': dt,
        'hour': hour,
        'razao': emp.razao.upper(),
        'endereco': emp.endereco.upper(),
        'tel': emp.tel,
        'clienteid': str(caixa.fk_tbcli.pk),
        'clientedsc': caixa.fk_tbcli.dsc.upper(),
        'tipopg': tipopg,
        'qtdparc': str(caixa.qtdparc),
        'subtotal': str(caixa.dvlr + desconto),
        'desconto': str(round(desconto, 2)),
        'totalgeral': str(caixa.dvlr),
        'userid': str(caixa.fk_user.pk),
        'userdsc': f'{caixa.fk_user.first_name} {caixa.fk_user.last_name}',
        'valorpago': valorpago if valorpago else str(caixa.dvlr),
        'troco': str(int(valorpago) - caixa.dvlr) if valorpago else '0'
    }

    vencimentos = {}

    if entradas:

        cont = 0

        for ent in entradas:

            cont += 1

            vencimentos['vencdt'] = f'{ent.dtvenc.day}/{ent.dtvenc.month}/{ent.dtvenc.year}'
            vencimentos['vencdvlr'] = str(ent.dvlrtotal)
            context[f'vencimento{cont}'] = vencimentos
            vencimentos = {}

    else:
        
        vencimentos['vencdt'] = dt
        vencimentos['vencdvlr'] = str(caixa.dvlr)
        context['vencimento1'] = vencimentos

    produtos = {}

    cont = 0

    for venda in vendas:

        cont += 1

        produtos['prodid'] = str(venda.fk_tbprod.pk)
        produtos['proddsc'] = str(venda.fk_tbprod.dsc)
        produtos['proddesconto'] = str((venda.fk_tbprod.dvlrvenda - venda.dvlr) * venda.qtd)
        produtos['prodqtd'] = str(venda.qtd)
        produtos['proddvlr'] = str(venda.dvlr)
        produtos['prodtotal'] = str(venda.dvlr * venda.qtd)
        context[f'produto{cont}'] = produtos
        produtos = {}

    context['qtdtotal'] = cont

    context_json = json.dumps(context)

    data = context_json.replace('"', "'")

    uri = f'print://?{data}'

    print(uri)

    return uri

def gerar_nf_consignado(request, consignado: TBCSG, tipopg):

    date = datetime.now()
    dt = str(date.date()).split('-')
    dt = f'{dt[2]}/{dt[1]}/{dt[0]}'
    hour = f'{date.hour}:{date.minute}'

    emp = CTBEMP.objects.latest('pk')

    vendas = TBIOCSG.objects.filter(fk_tbcsg = consignado)

    context = {
        'tipolayout': 2,
        'dt': dt,
        'hour': hour,
        'razao': emp.razao.upper(),
        'endereco': emp.endereco.upper(),
        'tel': emp.tel,
        'clienteid': str(consignado.fk_tbcli.pk),
        'clientedsc': consignado.fk_tbcli.dsc.upper(),
        'tipopg': tipopg,
        'devolucao': f'{consignado.dtfim.day}/{consignado.dtfim.month}/{consignado.dtfim.year}',
        'totalgeral': str(consignado.dvlr),
        'userid': str(consignado.fk_user.pk),
        'userdsc': f'{consignado.fk_user.first_name} {consignado.fk_user.last_name}',
    }

    produtos = {}

    cont = 0

    for venda in vendas:

        cont += 1

        produtos['prodid'] = str(venda.fk_tbprod.pk)
        produtos['proddsc'] = str(venda.fk_tbprod.dsc)
        produtos['prodqtd'] = str(venda.qtd)
        produtos['proddvlr'] = str(venda.fk_tbprod.dvlrvenda)
        produtos['prodtotal'] = str(venda.fk_tbprod.dvlrvenda * venda.qtd)
        context[f'produto{cont}'] = produtos
        produtos = {}

    context['qtdtotal'] = cont

    context_json = json.dumps(context)

    data = context_json.replace('"', "'")

    uri = f'print://?{data}'

    return uri

def gerar_relatorio_entrada(request):

    if not any([
        request.POST.get('dado_dteminicio'),
        request.POST.get('dado_dtemfim'),
        request.POST.get('dado_dtvencinicio'),
        request.POST.get('dado_dtvencfim'),
        request.POST.get('id_cliente'),
        request.POST.get('dado_status'),
    ]):
        
        error = 'Não é possível gerar um relatório sem filtros!'

    else:

        error = ''

        dteminicio = request.POST.get('dado_dteminicio')
        dtemfim = request.POST.get('dado_dtemfim')
        dtvencinicio = request.POST.get('dado_dtvencinicio')
        dtvencfim = request.POST.get('dado_dtvencfim')
        id_cliente = request.POST.get('id_cliente')
        status = request.POST.get('dado_status')

        object = TBIFIN.objects.all()

        if dteminicio:
            object = object.filter(dtem__date__gte = dteminicio)
        if dtemfim:
            object = object.filter(dtem__date__lte = dtemfim)
        if dtvencinicio:
            object = object.filter(dtvenc__date__gte = dtvencinicio)
        if dtvencfim:
            object = object.filter(dtvenc__date__lte = dtvencfim)
        if id_cliente:
            object = object.filter(fk_tbcli__pk = id_cliente)
        if status:
            object = object.filter(sts = status)

        if not object:

            error = 'O filtro escolhido não retornou dados!'

        else:

            pdf = PDF()
            pdf.set_font("Times", size=10)
            pdf.set_landscape()

            total = sum(i.dvlrtotal for i in object)

            data = [['Código', 'Número da Nota', 'Valor Total', 'Cliente', 'Data de Emissão', 'Data de Vencimento', 'Status']]

            cont = 0
            total_linhas = object.count()

            for obj in object:

                cont += 1

                linha = [
                    f'{obj.pk}',
                    f'{obj.numnota}', 
                    f'R$ {obj.dvlrtotal}', 
                    f'{obj.fk_tbcli.dsc}', 
                    f'{obj.dtem.day}/{obj.dtem.month}/{obj.dtem.year}', 
                    f'{obj.dtvenc.day}/{obj.dtvenc.month}/{obj.dtvenc.year}', 
                    f'{obj.get_sts_display()}'
                ]

                data.append(linha)

                if cont == 17:

                    total_linhas -= cont
                    cont = 0
            
                    pdf.create_table(table_data = data, title = 'BUDINO PUDINS', subtitle = 'Relatório de Contas a Receber', align_header = 'C', align_data = 'C', cell_width = 'even')
                    
                    data = [['Código', 'Número da Nota', 'Valor Total', 'Cliente', 'Data de Emissão', 'Data de Vencimento', 'Status']]

                if cont == total_linhas:

                    pdf.create_table(table_data = data, title = 'BUDINO PUDINS', subtitle = 'Relatório de Contas a Receber', align_header = 'C', align_data = 'C', cell_width = 'even')

            pdf.cell(270, 10, txt=f"Total: R$ {total}", ln=True, align='R')

            path = os.path.join(settings.MEDIA_ROOT, f'pdf/relatorio_contas_a_receber.pdf')

            pdf.output(path)

    return error

def gerar_relatorio_saida(request):

    if not any([
        request.POST.get('dado_dteminicio'),
        request.POST.get('dado_dtemfim'),
        request.POST.get('dado_dtvencinicio'),
        request.POST.get('dado_dtvencfim'),
        request.POST.get('id_fornecedor'),
        request.POST.get('dado_status'),
    ]):
        
        error = 'Não é possível gerar um relatório sem filtros!'

    else:

        error = ''

        dteminicio = request.POST.get('dado_dteminicio')
        dtemfim = request.POST.get('dado_dtemfim')
        dtvencinicio = request.POST.get('dado_dtvencinicio')
        dtvencfim = request.POST.get('dado_dtvencfim')
        id_fornecedor = request.POST.get('id_fornecedor')
        status = request.POST.get('dado_status')

        object = TBOFIN.objects.all()

        if dteminicio:
            object = object.filter(dtem__date__gte = dteminicio)
        if dtemfim:
            object = object.filter(dtem__date__lte = dtemfim)
        if dtvencinicio:
            object = object.filter(dtvenc__date__gte = dtvencinicio)
        if dtvencfim:
            object = object.filter(dtvenc__date__lte = dtvencfim)
        if id_fornecedor:
            object = object.filter(fk_tbforn__pk = id_fornecedor)
        if status:
            object = object.filter(sts = status)

        if not object:

            error = 'O filtro escolhido não retornou dados!'

        else:

            pdf = PDF()
            pdf.set_font("Times", size=10)
            pdf.set_landscape()

            total = sum(i.dvlrtotal for i in object)

            data = [['Código', 'Número da Nota', 'Valor Total', 'Fornecedor', 'Data de Emissão', 'Data de Vencimento', 'Status']]

            cont = 0
            total_linhas = object.count()

            for obj in object:

                cont += 1

                linha = [
                    f'{obj.pk}',
                    f'{obj.numnota}', 
                    f'R$ {obj.dvlrtotal}', 
                    f'{obj.fk_tbforn.razao}', 
                    f'{obj.dtem.day}/{obj.dtem.month}/{obj.dtem.year}', 
                    f'{obj.dtvenc.day}/{obj.dtvenc.month}/{obj.dtvenc.year}', 
                    f'{obj.get_sts_display()}'
                ]

                data.append(linha)

                if cont == 17:

                    total_linhas -= cont
                    cont = 0
            
                    pdf.create_table(table_data = data, title = 'BUDINO PUDINS', subtitle = 'Relatório de Contas a Pagar', align_header = 'C', align_data = 'C', cell_width = 'even')
                    
                    data = [['Código', 'Número da Nota', 'Valor Total', 'Fornecedor', 'Data de Emissão', 'Data de Vencimento', 'Status']]

                if cont == total_linhas:

                    pdf.create_table(table_data = data, title = 'BUDINO PUDINS', subtitle = 'Relatório de Contas a Pagar', align_header = 'C', align_data = 'C', cell_width = 'even')

            pdf.cell(270, 10, txt=f"Total: R$ {total}", ln=True, align='R')

            path = os.path.join(settings.MEDIA_ROOT, f'pdf/relatorio_contas_a_pagar.pdf')

            pdf.output(path)

    return error

def gerar_relatorio_caixa(request):

    if not any([
        request.POST.get('dado_dtinicio'),
        request.POST.get('dado_dtfim'),
        request.POST.get('id_usuario'),
        request.POST.get('id_cliente'),
    ]):
        
        error = 'Não é possível gerar um relatório sem filtros!'

    else:

        error = ''

        dtinicio = request.POST.get('dado_dtinicio')
        dtfim = request.POST.get('dado_dtfim')
        id_usuario = request.POST.get('id_usuario')
        id_cliente = request.POST.get('id_cliente')

        object = TBCX.objects.all()

        if dtinicio:
            object = object.filter(dt__date__gte = dtinicio)
        if dtfim:
            object = object.filter(dt__date__lte = dtfim)
        if id_usuario:
            object = object.filter(fk_user__pk = id_usuario)
        if id_cliente:
            object = object.filter(fk_tbcli__pk = id_cliente)

        if not object:

            error = 'O filtro escolhido não retornou dados!'

        else:

            pdf = PDF()
            pdf.set_font("Times", size=10)
            pdf.set_landscape()

            total = sum(i.dvlr for i in object)

            data = [['Código', 'Valor Total', 'Vendedor', 'Cliente', 'Tipo de Pagamento', 'Data']]

            cont = 0
            total_linhas = object.count()

            for obj in object:

                cont += 1

                if obj.fk_ctbitipopg:
                    tipopg = obj.fk_ctbitipopg.dsc
                elif obj.qtdparc > 1:
                    tipopg = 'Crediário'
                else:
                    tipopg = 'Dinheiro'

                linha = [
                    f'{obj.pk}',
                    f'R$ {obj.dvlr}', 
                    f'{obj.fk_user.first_name} {obj.fk_user.last_name}', 
                    f'{obj.fk_tbcli.dsc}', 
                    f'{tipopg}',
                    f'{obj.dt.day}/{obj.dt.month}/{obj.dt.year}'
                ]

                data.append(linha)

                if cont == 17:

                    total_linhas -= cont
                    cont = 0
            
                    pdf.create_table(table_data = data, title = 'BUDINO PUDINS', subtitle = 'Relatório de Caixa', align_header = 'C', align_data = 'C', cell_width = 'even')
                    
                    data = [['Código', 'Valor Total', 'Vendedor', 'Cliente', 'Tipo de Pagamento', 'Data']]

                if cont == total_linhas:

                    pdf.create_table(table_data = data, title = 'BUDINO PUDINS', subtitle = 'Relatório de Caixa', align_header = 'C', align_data = 'C', cell_width = 'even')

            pdf.cell(270, 10, txt=f"Total: R$ {total}", ln=True, align='R')

            path = os.path.join(settings.MEDIA_ROOT, f'pdf/relatorio_caixa.pdf')

            pdf.output(path)

    return error





