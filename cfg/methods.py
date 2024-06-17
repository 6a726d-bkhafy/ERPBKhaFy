from django.contrib.auth.models import User, Permission
from .models import *

def editar_senha_usuario(request):

    senha = request.POST.get('dado_senha')
    user = User.objects.get(pk = request.POST.get('id_user'))

    user.set_password(senha)
    user.save()

def criar_novo_usuario(request):

    first_name = request.POST.get('dado_first_name')
    last_name = request.POST.get('dado_last_name')
    username = request.POST.get('dado_user')
    email = request.POST.get('dado_email')
    senha = request.POST.get('dado_senha')
    is_admin = request.POST.get('dado_is_admin')

    user = User(
        username = username,
        first_name = first_name,
        last_name = last_name,
        email = email,
        is_superuser = True if is_admin == 'on' else False
    )
    user.set_password(senha)
    user.save()

    return user

def criar_profile_para_usuario(user: User):

    profile = CTBPROFILE(
        fk_user = user,
        avatar = 'avatar/default.png'
    )
    profile.save()

def editar_usuario_existente(request):

    user = User.objects.get(pk = request.POST.get('id_user'))
    first_name = request.POST.get('dado_first_name')
    last_name = request.POST.get('dado_last_name')
    username = request.POST.get('dado_user')
    email = request.POST.get('dado_email')
    is_admin = request.POST.get('dado_is_admin')

    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.email = email
    user.is_superuser = True if is_admin == 'on' else False

    user.save()

def criar_nova_categoria(request):

    dsc = request.POST.get('dado_dsc')

    categoria = CTBCATPROD(
        dsc = dsc
    )
    categoria.save()

def editar_categoria_existente(request):

    dsc = request.POST.get('dado_dsc')
    categoria = CTBCATPROD.objects.get(pk = request.POST.get('id_categoria'))

    categoria.dsc = dsc
    categoria.save()

def criar_novo_custo(request):

    dsc = request.POST.get('dado_dsc')

    custo = CTBCATFIN(
        dsc = dsc
    )
    custo.save()

def editar_custo_existente(request):

    dsc = request.POST.get('dado_dsc')
    custo = CTBCATFIN.objects.get(pk = request.POST.get('id_custo'))

    custo.dsc = dsc
    custo.save()

def criar_novo_juro(request):

    pvlr = request.POST.get('dado_pvlr')

    juro = CTBJURO(
        pvlr = pvlr
    )
    juro.save()

def editar_juro_existente(request):

    pvlr = request.POST.get('dado_pvlr')
    juro = CTBJURO.objects.get(pk = request.POST.get('id_juro'))

    juro.pvlr = pvlr
    juro.save()

def criar_nova_conta(request):

    razao = request.POST.get('dado_razao')
    banco = request.POST.get('dado_banco')
    ag = request.POST.get('dado_agencia')
    conta_bancaria = request.POST.get('dado_conta')
    pix = request.POST.get('dado_pix')

    conta_bancaria = CTBBANK(
        razao = razao,
        banco = banco,
        ag = ag,
        conta = conta_bancaria,
        pix = pix
    )
    conta_bancaria.save()

def editar_conta_existente(request):

    conta_bancaria = CTBBANK.objects.get(pk = request.POST.get('id_conta_bancaria'))

    razao = request.POST.get('dado_razao')
    banco = request.POST.get('dado_banco')
    ag = request.POST.get('dado_agencia')
    conta = request.POST.get('dado_conta')
    pix = request.POST.get('dado_pix')

    conta_bancaria.razao = razao
    conta_bancaria.banco = banco
    conta_bancaria.ag = ag
    conta_bancaria.conta = conta
    conta_bancaria.pix = pix
    conta_bancaria.save()

def criar_novo_tipopg(request):

    dsc = request.POST.get('dado_dsc')
    conta = CTBBANK.objects.get(pk = request.POST.get('id_conta'))

    tipopg = CTBITIPOPG(
        dsc = dsc,
        fk_ctbbank = conta
    )
    tipopg.save()

def editar_tipopg_existente(request):

    dsc = request.POST.get('dado_dsc')
    conta = CTBBANK.objects.get(pk = request.POST.get('id_conta'))
    tipopg = CTBITIPOPG.objects.get(pk = request.POST.get('id_tipopg'))

    tipopg.dsc = dsc
    tipopg.fk_ctbbank = conta
    tipopg.save()

def definir_acessos(request):

    user = User.objects.get(pk = request.POST.get('id_user'))
    check_consignado = request.POST.get('check_consignado')
    check_etiquetas = request.POST.get('check_etiquetas')
    check_inventarios = request.POST.get('check_inventarios')
    check_produtos = request.POST.get('check_produtos')
    check_troca = request.POST.get('check_troca')
    check_saida = request.POST.get('check_saida')
    check_entrada = request.POST.get('check_entrada')
    check_caixa = request.POST.get('check_caixa')
    check_transf = request.POST.get('check_transf')
    check_compras = request.POST.get('check_compras')
    check_lote = request.POST.get('check_lote')
    check_clientes = request.POST.get('check_clientes')
    check_fornecedores = request.POST.get('check_fornecedores')
    check_categorias = request.POST.get('check_categorias')
    check_contas = request.POST.get('check_contas')
    check_juros = request.POST.get('check_juros')
    check_custos = request.POST.get('check_custos')
    check_pagamentos = request.POST.get('check_pagamentos')
    check_usuarios = request.POST.get('check_usuarios')
    check_pdv = request.POST.get('check_pdv')

    if check_consignado:
        user.user_permissions.add(Permission.objects.get(codename = 'view_consignado'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_consignado'))
    if check_etiquetas:
        user.user_permissions.add(Permission.objects.get(codename = 'view_etiquetas'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_etiquetas'))
    if check_inventarios:
        user.user_permissions.add(Permission.objects.get(codename = 'view_inventarios'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_inventarios'))
    if check_produtos:
        user.user_permissions.add(Permission.objects.get(codename = 'view_produtos'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_produtos'))
    if check_troca:
        user.user_permissions.add(Permission.objects.get(codename = 'view_troca'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_troca'))
    if check_saida:
        user.user_permissions.add(Permission.objects.get(codename = 'view_saida'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_saida'))
    if check_entrada:
        user.user_permissions.add(Permission.objects.get(codename = 'view_entrada'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_entrada'))
    if check_caixa:
        user.user_permissions.add(Permission.objects.get(codename = 'view_caixa'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_caixa'))
    if check_transf:
        user.user_permissions.add(Permission.objects.get(codename = 'view_transf'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_transf'))
    if check_compras:
        user.user_permissions.add(Permission.objects.get(codename = 'view_compra'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_compra'))
    if check_lote:
        user.user_permissions.add(Permission.objects.get(codename = 'view_lote'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_lote'))
    if check_clientes:
        user.user_permissions.add(Permission.objects.get(codename = 'view_clientes'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_clientes'))
    if check_fornecedores:
        user.user_permissions.add(Permission.objects.get(codename = 'view_fornecedores'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_fornecedores'))
    if check_categorias:
        user.user_permissions.add(Permission.objects.get(codename = 'view_categorias'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_categorias'))
    if check_contas:
        user.user_permissions.add(Permission.objects.get(codename = 'view_contas'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_contas'))
    if check_juros:
        user.user_permissions.add(Permission.objects.get(codename = 'view_juros'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_juros'))
    if check_custos:
        user.user_permissions.add(Permission.objects.get(codename = 'view_custos'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_custos'))
    if check_pagamentos:
        user.user_permissions.add(Permission.objects.get(codename = 'view_pagamentos'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_pagamentos'))
    if check_usuarios:
        user.user_permissions.add(Permission.objects.get(codename = 'view_usuarios'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_usuarios'))
    if check_pdv:
        user.user_permissions.add(Permission.objects.get(codename = 'view_pdv'))
    else:
        user.user_permissions.remove(Permission.objects.get(codename = 'view_pdv'))
