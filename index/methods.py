from django.urls import reverse
from django.http import JsonResponse
from estoque.models import TBPROD
from parceiros.models import TBFORN, TBCLI
from cfg.models import CTBPROFILE, CTBCATPROD, CTBCATFIN
from django.contrib.auth.models import User
from financeiro.models import TBIFIN, TBOPG, TBIPG, TBCX, TBOPROD, TBOFIN
from django.db.models.query import Q
from datetime import datetime, timedelta
from django.db.models import Min

def atualizar_imagem_do_perfil(request):

    avatar = request.FILES['dado_avatar']
    avatar.name = f'{request.user.pk}.png'
    profile = CTBPROFILE.objects.get(fk_user = request.user)
    profile.avatar = avatar
    profile.save()

def buscar_por_tela(request):

    urls = {}

    if request.user.has_perm('estoque.view_consignado'):
        urls['sc_list_consignado'] = reverse('sc_list_consignado')
    if request.user.has_perm('estoque.view_etiquetas'):
        urls['sc_insert_etiqueta'] = reverse('sc_insert_etiqueta')
    if request.user.has_perm('estoque.view_inventarios'):
        urls['sc_list_inventario'] = reverse('sc_list_inventario')
    if request.user.has_perm('estoque.view_produtos'):
        urls['sc_list_produto'] = reverse('sc_list_produto')
    if request.user.has_perm('estoque.view_troca'):
        urls['sc_list_troca'] = reverse('sc_list_troca')
    if request.user.has_perm('financeiro.view_saida'):
        urls['sc_list_saida_financeiro'] = reverse('sc_list_saida_financeiro')
    if request.user.has_perm('financeiro.view_entrada'):
        urls['sc_list_entrada_financeiro'] = reverse('sc_list_entrada_financeiro')
    if request.user.has_perm('financeiro.view_caixa'):
        urls['sc_list_caixa'] = reverse('sc_list_caixa')
    if request.user.has_perm('financeiro.view_transf'):
        urls['sc_list_transf'] = reverse('sc_list_transf')
    if request.user.has_perm('compras.view_compras'):
        urls['sc_list_compra'] = reverse('sc_list_compra')
    if request.user.has_perm('parceiros.view_clientes'):
        urls['sc_list_cliente'] = reverse('sc_list_cliente')
    if request.user.has_perm('parceiros.view_fornecedores'):
        urls['sc_list_fornecedor'] = reverse('sc_list_fornecedor')
    if request.user.has_perm('cfg.view_categorias'):
        urls['sc_list_categoria'] = reverse('sc_list_categoria')
    if request.user.has_perm('cfg.view_contas'):
        urls['sc_list_conta'] = reverse('sc_list_conta')
    if request.user.has_perm('cfg.view_juros'):
        urls['sc_list_juro'] = reverse('sc_list_juro')
    if request.user.has_perm('cfg.view_custos'):
        urls['sc_list_custo'] = reverse('sc_list_custo')
    if request.user.has_perm('cfg.view_pagamentos'):
        urls['sc_list_tipopg'] = reverse('sc_list_tipopg')
    if request.user.has_perm('cfg.view_usuarios'):
        urls['sc_list_user'] = reverse('sc_list_user')
    if request.user.has_perm('financeiro.view_pdv'):
        urls['sc_insert_pdv'] = reverse('sc_insert_pdv')

    return JsonResponse(urls)

def buscar_produto_por_pk(pk):

    try:

        produto = TBPROD.objects.get(pk = pk)

        data = {
            'pk': produto.pk,
            'desc': produto.dsc
        }

    except:

        data = {
            'pk': 0,
            'desc': 'Não Encontrado'
        }

    return JsonResponse(data)

def buscar_produto_por_desc(request):

    query = request.GET.get('term', '')
    produto = TBPROD.objects.filter(dsc__icontains = query)

    results = [
        {
            'pk': i.pk,
            'desc': i.dsc,
            'value': i.dsc,
        }
        for i in produto
    ]

    return JsonResponse(results, safe = False)

def buscar_fornecedor_por_pk(pk):

    try:

        fornecedor = TBFORN.objects.get(pk = pk)

        data = {
            'pk': fornecedor.pk,
            'desc': fornecedor.razao
        }

    except:

        data = {
            'pk': 0,
            'desc': 'Não Encontrado'
        }

    return JsonResponse(data)

def buscar_fornecedor_por_desc(request):

    query = request.GET.get('term', '')
    fornecedor = TBFORN.objects.filter(razao__icontains = query)

    results = [
        {
            'pk': i.pk,
            'desc': i.razao,
            'value': i.razao,
        }
        for i in fornecedor
    ]

    return JsonResponse(results, safe = False)

def buscar_cliente_por_pk(pk):

    try:

        cliente = TBCLI.objects.get(pk = pk)

        entradas = TBIFIN.objects.filter(
            Q(fk_tbcli = cliente) &
            (
                Q(sts = '0') |
                Q(sts = '2') |
                Q(sts = '4')
            ) &
            Q(dtvenc__lt = datetime.now().date())
        )

        pend = sum(ent.dvlrpend for ent in entradas)

        data = entradas.aggregate(Min('dtvenc'))['dtvenc__min']

        if data:
            atraso = datetime.now() - data
            atraso = atraso.days
        else:
            atraso = 0

        data = {
            'pk': cliente.pk,
            'dsc': cliente.dsc,
            'limite': cliente.limite,
            'creddisp': cliente.creddisp,
            'consdisp': cliente.consdisp,
            'dvlrpend': pend,
            'atraso': atraso
        }
    
    except:

        data = {
            'pk': 0,
            'dsc': 'Não Encontrado',
            'limite': 0,
            'creddisp': 0,
            'consdisp': 0,
            'dvlrpend': 0,
            'atraso': 0
        }

    return JsonResponse(data)

def buscar_cliente_por_desc(request):

    query = request.GET.get('term', '')
    cliente = TBCLI.objects.filter(dsc__icontains = query)

    pend_dict = {}
    atraso_dict = {}

    for cli in cliente:

        entradas = TBIFIN.objects.filter(
            Q(fk_tbcli = cli) &
            (
                Q(sts = '0') |
                Q(sts = '2') |
                Q(sts = '4')
            ) &
            Q(dtvenc__lt = datetime.now().date())
        )

        pend_dict[cli] = sum(ent.dvlrpend for ent in entradas if ent.fk_tbcli)

        data = entradas.aggregate(Min('dtvenc'))['dtvenc__min']

        if data:
            atraso = datetime.now() - data
            atraso = atraso.days
        else:
            atraso = 0

        atraso_dict[cli] = atraso

    results = [
        {
            'pk': cli.pk,
            'desc': cli.dsc,
            'limite': cli.limite,
            'creddisp': cli.creddisp,
            'consdisp': cli.consdisp,
            'dvlrpend': pend_dict.get(cli),
            'atraso': atraso_dict.get(cli),
            'value': cli.dsc
        }
        for cli in cliente
    ]

    return JsonResponse(results, safe = False)

def buscar_usuario_por_pk(pk):

    try:

        user = User.objects.get(pk = pk)

        data = {
            'pk': user.pk,
            'username': f'{user.first_name} {user.last_name}'
        }

    except:

        data = {
            'pk': 0,
            'username': 'Não Encontrado'
        }

    return JsonResponse(data)

def buscar_usuario_por_desc(request):

    query = request.GET.get('term', '')
    user = User.objects.filter(first_name__icontains = query)

    results = [
        {
            'pk': i.pk,
            'username': f'{i.first_name} {i.last_name}',
            'value': f'{i.first_name} {i.last_name}',
        }
        for i in user
    ]

    return JsonResponse(results, safe = False)

def grafico_vendas_data(parameter):

    if parameter == 2:

        dates_pg = []
        dates_rec = []
        dates_cx = []
        
        for i in range(0, 12):

            mes = datetime.now().month - i
            ano = datetime.now().year

            if mes <= 0:
                mes += 12
                ano -= 1

            dates_pg.append((ano, mes))
            dates_rec.append((ano, mes))
            dates_cx.append((ano, mes))

    else:
        limite = datetime.now() - timedelta(days = 30)

        pgs = TBOPG.objects.filter(dtpg__gte = limite)
        dates_pg = [pg.dtpg.date() for pg in pgs]
        dates_pg = list(set(dates_pg))
        dates_pg.sort()

        recs = TBIPG.objects.filter(dtpg__gte = limite)
        dates_rec = [rec.dtpg.date() for rec in recs]
        dates_rec = list(set(dates_rec))
        dates_rec.sort()

        cxs = TBCX.objects.filter(dt__gte = limite)
        dates_cx = [cx.dt.date() for cx in cxs]
        dates_cx = list(set(dates_cx))
        dates_cx.sort()

    pagamentos = []

    for dt in dates_pg:

        if parameter == 2:
            pgs = TBOPG.objects.filter(dtpg__month = dt[1], dtpg__year = dt[0])
        else:
            pgs = TBOPG.objects.filter(dtpg__icontains = dt)
        total = sum(pg.dvlr for pg in pgs)

        pg_dict = {
            'date': dt,
            'value': total
        }

        pagamentos.append(pg_dict)

    recebimentos = []

    for dt in dates_rec:

        if parameter == 2:
            recs = TBIPG.objects.filter(dtpg__month = dt[1], dtpg__year = dt[0])
        else:
            recs = TBIPG.objects.filter(dtpg__icontains = dt)
        total = sum(rec.dvlr for rec in recs)

        rec_dict = {
            'date': dt,
            'value': total
        }

        recebimentos.append(rec_dict)

    vendas = []

    for dt in dates_cx:

        if parameter == 2:
            cxs = TBCX.objects.filter(dt__month = dt[1], dt__year = dt[0])
        else:
            cxs = TBCX.objects.filter(dt__icontains = dt)
        total = sum(cx.dvlr for cx in cxs)

        cx_dict = {
            'date': dt,
            'value': total
        }

        vendas.append(cx_dict)

    data = {
        'Vendas': vendas,
        'Recebimentos': recebimentos,
        'Pagamentos': pagamentos
    }

    return JsonResponse(data)

def grafico_categorias_data(parameter):

    if parameter == 2:
        limite = datetime.now() - timedelta(days = 30)
    if parameter == 3:
        limite = datetime.now() - timedelta(days = 365)
    else:
        limite = datetime.now() - timedelta(days = 7)

    categorias = TBPROD.objects.all()

    data = []

    for cat in categorias:

        total = TBOPROD.objects.filter(fk_tbprod = cat, fk_tbcx__dt__gte = limite).count()

        cat_dict = {
            'value': total if total else 0,
            'name': cat.dsc
        }

        data.append(cat_dict)

    return JsonResponse(data, safe = False)

def grafico_custos_data(parameter):

    if parameter == 2:
        limite = datetime.now() - timedelta(days = 30)
    if parameter == 3:
        limite = datetime.now() - timedelta(days = 365)
    else:
        limite = datetime.now() - timedelta(days = 7)

    custos = CTBCATFIN.objects.all()

    data = []

    for custo in custos:

        total = sum(i.dvlrtotal for i in TBOFIN.objects.filter(Q(fk_ctbcatfin = custo, dtem__gte = limite) & ~Q(sts = '3')))

        custo_dict = {
            'value': total,
            'name': custo.dsc
        }

        data.append(custo_dict)

    return JsonResponse(data, safe = False)