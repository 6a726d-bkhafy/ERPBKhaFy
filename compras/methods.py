from parceiros.models import TBFORN
from .models import *
from estoque.models import TBPROD, STBPPROD
from datetime import datetime
from decimal import Decimal
from financeiro.models import TBOFIN
from cfg.models import CTBCATFIN
import calendar
from index.pdf_creator.create_table_fpdf2 import PDF
import os
from django.conf import settings

def criar_nova_ordem(request, fk):

    qtd = int(request.POST.get('dado_qtd'))
    valor = Decimal(request.POST.get('dado_valor'))

    if fk == 0:

        fornecedor = TBFORN.objects.get(pk = request.POST.get('id_fornecedor'))
        custo = CTBCATFIN.objects.get(pk = request.POST.get('id_custo'))
        numnota = request.POST.get('dado_numnota')
        tipomov = '2'
        dtvenc = request.POST.get('dado_dtvenc')
        dtem = request.POST.get('dado_dtem')
        user = request.user
        parcelas = request.POST.get('dado_parcela')

        ordem = TBCOMP(
            fk_tbforn = fornecedor,
            tipomov = tipomov,
            qtd = qtd,
            dvlr = valor * qtd,
            fk_user = user,
            dt = datetime.now(),
            sts = '0',
            fk_ctbcatfin = custo,
            numnota = numnota,
            dtvenc = dtvenc,
            dtem = dtem,
            qtdparc = parcelas
        )
        ordem.save()

    else:

        ordem = TBCOMP.objects.get(pk = fk)
        ordem.qtd += qtd
        ordem.dvlr += valor * qtd
        ordem.save()

    return ordem

def adicionar_produto_a_lista(request, ordem):

    produto = TBPROD.objects.get(pk = request.POST.get('id_produto'))
    qtd = request.POST.get('dado_qtd')
    valor = request.POST.get('dado_valor')

    lista_ordem = STBICOMP(
        fk_tbcomp = ordem,
        fk_tbprod = produto,
        qtd = qtd,
        dvlr = valor
    )
    lista_ordem.save()

def excluir_produto_da_lista(request):

    compra = STBICOMP.objects.get(pk = request.POST.get('id_compra'))
    ordem = compra.fk_tbcomp

    ordem.qtd -= compra.qtd
    ordem.dvlr -= compra.dvlr * compra.qtd
    ordem.save()
    compra.delete()

def excluir_todos_os_produtos_da_lista(fk):

    ordem = TBCOMP.objects.get(pk = fk)
    compras = STBICOMP.objects.filter(fk_tbcomp = ordem)
    compras.delete()

    ordem.qtd = 0
    ordem.dvlr = 0
    ordem.save()

def excluir_todos_os_produtos_da_lista_lote(fk):

    ordem = TBLOTE.objects.get(pk = fk)
    compras = STBILOTE.objects.filter(fk_tblote = ordem)
    compras.delete()

    ordem.qtd = 0
    ordem.save()

def alterar_quantidade_de_um_produto(request):

    compra = STBICOMP.objects.filter(pk = request.POST.get('id_compra'))
    ordem = compra[0].fk_tbcomp
    qtd = int(request.POST.get('dado_qtd'))

    ordem.dvlr = (ordem.dvlr / ordem.qtd) * qtd

    if qtd > compra[0].qtd:
        ordem.qtd += qtd - compra[0].qtd
    else:
        ordem.qtd -= compra[0].qtd - qtd
    
    ordem.save()
    compra.update(qtd = qtd)

def criar_entrada_de_produto(fk):

    ordem = TBCOMP.objects.get(pk = fk)
    compras = STBICOMP.objects.filter(fk_tbcomp = ordem)

    entradas = []

    for compra in compras:

        entrada = TBIPROD(
            fk_tbcomp = compra.fk_tbcomp,
            fk_tbprod = compra.fk_tbprod,
            qtd = compra.qtd,
            qtdpen = compra.qtd,
            dvlr = compra.dvlr,
            sts = 0
        )
        entradas.append(entrada)
        
    TBIPROD.objects.bulk_create(entradas)
    compras.delete()

    return ordem

def criar_entrada_de_lote(fk):

    lt = TBLOTE.objects.get(pk = fk)
    lotes = STBILOTE.objects.filter(fk_tblote = lt)

    entradas = []

    for lote in lotes:

        entra = TBILOTE(
            fk_tblote = lote.fk_tblote,
            fk_tbprod = lote.fk_tbprod,
            qtd = lote.qtd,
        )
        entradas.append(entra)
        
    TBILOTE.objects.bulk_create(entradas)
    lotes.delete()

    return lt

def criar_lancamento_financeiro(ordem: TBCOMP):

    dt = datetime.strptime(str(ordem.dtvenc.date()), "%Y-%m-%d")

    parcela = ordem.dvlr / ordem.qtdparc
    parcela = round(parcela, 2)

    for i in range(ordem.qtdparc):

        saida_fin = TBOFIN(
            fk_tbforn = ordem.fk_tbforn,
            dvlrtotal = parcela,
            dvlrpend = parcela,
            fk_ctbcatfin = ordem.fk_ctbcatfin,
            dtem = ordem.dtem,
            dtvenc = dt,
            sts = '0',
            comprod = True,
            numnota = ordem.numnota,
            tipoop = ordem.tipomov,
            fk_tbcomp = ordem
        )
        saida_fin.save()

        ano = dt.year
        mes = dt.month + 1
        if mes > 12:
            mes = 1
            ano += 1

        ultimo_dia_do_mes = calendar.monthrange(ano, mes)[1]
        dia = min(dt.day, ultimo_dia_do_mes)

        dt = datetime(ano, mes, dia)

    ordem.sts = '1'
    ordem.save()

def alterar_sts_lote(ordem: TBCOMP):
    ordem.sts = '1'
    ordem.save()

def realizar_entrada(request):

    ordem = TBCOMP.objects.get(pk = request.POST.get('id_compra'))
    entradas = TBIPROD.objects.filter(fk_tbcomp = ordem)

    for ent in entradas:

        produto = ent.fk_tbprod
        qtd = int(request.POST.get(f'dado_{ent.fk_tbprod.pk}')) if request.POST.get(f'dado_{ent.fk_tbprod.pk}') else 0

        if ordem.tipomov == 1:

            produto.qtdestoque += qtd
            produto.qtdvstg += qtd

        elif ordem.tipomov == 2:

            produto.qtdestoque += qtd

        else:

            produto.qtdvstg += qtd

        produto.dvlrcusto = round(ent.dvlr, 2)

        if ent.dvlr + (ent.dvlr * produto.pvlrmmin / 100) > produto.dvlrvenda:

            produto.dvlrvenda = round(ent.dvlr + (ent.dvlr * produto.pvlrmmin / 100), 2)
            produto.pvlrmatual = produto.pvlrmmin

        else:

            margem = produto.dvlrvenda / produto.dvlrcusto
            porcentagem = round(100 * (margem - 1), 2)
            produto.pvlrmatual = porcentagem

        ent.qtdpen -= qtd
        ent.sts = '1' if ent.qtdpen == 0 else '0'
        produto.save()
        ent.save()

    return ordem, entradas

def realizar_entrada_lote(request):

    ordem = TBLOTE.objects.get(pk = request.POST.get('id_lote'))
    entradas = TBILOTE.objects.filter(fk_tblote = ordem)

    for ent in entradas:

        produto = ent.fk_tbprod
        qtdp = int(request.POST.get(f'dado_{ent.fk_tbprod.pk}')) if request.POST.get(f'dado_{ent.fk_tbprod.pk}') else 0
        produto.qtdestoque += qtdp
        produto.save()
        ent.save()
    
    return ordem, entradas

def validar_status_da_ordem(ordem, entradas):

    qtdtotal = 0

    for ent in entradas:

        qtdtotal += ent.qtdpen

    if qtdtotal == 0:

        ordem.sts = '3'
        ordem.save()
    
    elif qtdtotal < ordem.qtd:

        ordem.sts = '2'
        ordem.save()

def validar_status_do_lote(ordem, entradas):

    ordem.sts = '3'
    ordem.save()

def realizar_estorno_de_compra(request):

    compra = TBCOMP.objects.get(pk = request.POST.get('id_compra'))
    fin = TBOFIN.objects.get(fk_tbcomp = compra)
    fin.sts = '3'
    fin.save()

    compra.sts = '4'
    compra.save()

    TBIPROD.objects.filter(fk_tbcomp = compra).update(sts = '2')

def realizar_estorno_de_lote(request):

    lote = TBLOTE.objects.get(pk = request.POST.get('id_lote'))
    lote.sts = '4'
    lote.save()

def gerar_etiquetas(request):

    produtos = TBIPROD.objects.filter(fk_tbcomp__pk = request.POST.get('id_ordem'))

    print(request.POST.get('id_ordem'))

    STBPPROD.objects.filter(fk_user = request.user).delete()

    list_etiquetas = []

    for prod in produtos:

        etiqueta = STBPPROD(
            fk_tbprod = prod.fk_tbprod,
            qtd = prod.qtd,
            fk_user = request.user
        )
        list_etiquetas.append(etiqueta)

    STBPPROD.objects.bulk_create(list_etiquetas)

def gerar_relatorio_compra(request):

    if not any([
        request.POST.get('dado_dtinicio'),
        request.POST.get('dado_dtfim'),
        request.POST.get('id_fornecedor')
    ]):
        
        error = 'Não é possível gerar um relatório sem filtros!'

    else:

        error = ''

        dtinicio = request.POST.get('dado_dtinicio')
        dtfim = request.POST.get('dado_dtfim')
        id_fornecedor = request.POST.get('id_fornecedor')

        object = TBCOMP.objects.all()

        if dtinicio:
            object = object.filter(dt__date__gte = dtinicio)
        if dtfim:
            object = object.filter(dt__date__lte = dtfim)
        if id_fornecedor:
            object = object.filter(fk_tbforn__pk = id_fornecedor)

        if not object:

            error = 'O filtro escolhido não retornou dados!'

        else:

            pdf = PDF()
            pdf.set_font("Times", size=10)
            pdf.set_landscape()

            total = sum(i.dvlr for i in object)

            data = [['Fornecedor', 'Total de Itens', 'Valor Total', 'Data de Abertura']]

            cont = 0
            total_linhas = object.count()

            for obj in object:

                cont += 1

                linha = [
                    f'{obj.fk_tbforn.razao}',
                    f'{obj.qtd}', 
                    f'R$ {obj.dvlr}', 
                    f'{obj.dt.day}/{obj.dt.month}/{obj.dt.year}'
                ]

                data.append(linha)

                if cont == 17:

                    total_linhas -= cont
                    cont = 0
            
                    pdf.create_table(table_data = data, title = 'SAVANA STORE', subtitle = 'Relatório de Compra', align_header = 'C', align_data = 'C', cell_width = 'even')
                    
                    data = [['Fornecedor', 'Total de Itens', 'Valor Total', 'Data de Abertura']]

                if cont == total_linhas:

                    pdf.create_table(table_data = data, title = 'SAVANA STORE', subtitle = 'Relatório de Compra', align_header = 'C', align_data = 'C', cell_width = 'even')

            pdf.cell(270, 10, txt=f"Total: R$ {total}", ln=True, align='R')

            path = os.path.join(settings.MEDIA_ROOT, f'pdf/relatorio_compra.pdf')

            pdf.output(path)

    return error

def criar_nova_ordem_lote(request, fk):

    qtd = int(request.POST.get('dado_qtd'))

    if fk == 0:

        user = request.user

        ordem = TBLOTE(
            qtd = qtd,
            fk_user = user,
            dt = datetime.now(),
            sts = '0',
        )
        ordem.save()

    else:

        ordem = TBLOTE.objects.get(pk = fk)
        ordem.qtd += qtd
        ordem.save()

    return ordem

def adicionar_produto_a_lista_lote(request, ordem):

    produto = TBPROD.objects.get(pk = request.POST.get('id_produto'))
    qtd = request.POST.get('dado_qtd')

    lista_ordem = STBILOTE(
        fk_tblote = ordem,
        fk_tbprod = produto,
        qtd = qtd,
    )
    lista_ordem.save()