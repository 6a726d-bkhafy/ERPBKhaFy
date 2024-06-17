from .models import *
from decimal import Decimal
from datetime import datetime


def criar_novo_cliente(request):

    dsc = request.POST.get('dado_dsc')
    tipocli = request.POST.get('dado_tipocli')
    doc = request.POST.get('dado_doc')
    rg = request.POST.get('dado_rg')
    limite = request.POST.get('dado_limite')
    dtnasc = request.POST.get('dado_dtnasc')
    email = request.POST.get('dado_email')
    tel1 = request.POST.get('dado_tel1')
    tel2 = request.POST.get('dado_tel2')
    telrec = request.POST.get('dado_telrec')
    teltrab = request.POST.get('dado_teltrab')
    celular = request.POST.get('dado_celular')
    contato = request.POST.get('dado_contato')
    localtrab = request.POST.get('dado_localtrab')
    dttrab = request.POST.get('dado_dttrab')
    bairro = request.POST.get('dado_bairro')
    num = request.POST.get('dado_num')
    estado = request.POST.get('dado_estado')
    cidade = request.POST.get('dado_cidade')
    rua = request.POST.get('dado_rua')
    ref1 = request.POST.get('dado_ref1')
    ref2 = request.POST.get('dado_ref2')
    ref3 = request.POST.get('dado_ref3')
    obs = request.POST.get('dado_obs')

    parceiro = TBCLI(
        dsc = dsc,
        tipocli = tipocli,
        doc = doc,
        rg = rg,
        limite = limite,
        dtnasc = dtnasc if dtnasc else None,
        email = email,
        tel1 = tel1,
        tel2 = tel2,
        telrec = telrec,
        teltrab = teltrab,
        celular = celular,
        contato = contato,
        localtrab = localtrab,
        dttrab = dttrab if dttrab else None,
        bairro = bairro,
        num = num,
        estado = estado,
        cidade = cidade,
        rua = rua,
        ref1 = ref1,
        ref2 = ref2,
        ref3 = ref3,
        obs = obs,
        dtcad = datetime.now(),
        consdisp = limite,
        creddisp = limite
    )
    parceiro.save()

    if 'dado_img' in request.FILES:
        img = request.FILES['dado_img']
        img.name = f'{parceiro.pk}.png'
        parceiro.img = img
        parceiro.save()

def criar_novo_agenda_cliente(request):

    dthr = request.POST.get('dado_dthr')
    stscli = request.POST.get('dado_stscli')
    tpcli = request.POST.get('dado_tpcli')
    usr = User.objects.get(pk = request.POST.get('id_usuario_cred'))
    cli = TBCLI.objects.get(pk = request.POST.get('id_cliente_cred'))
    resp = request.POST.get('dado_resp')
    ass = request.POST.get('dado_ass')
    dsc = request.POST.get('dado_dsc')

    agendacli = TBAGENDACLI(
        dthr = dthr,
        stsagendacli = stscli,
        tipocontatocli = tpcli,
        fk_user = usr,
        fk_tbcli = cli,
        resp = resp,
        assunto = ass,
        dsc = dsc,
    )
    agendacli.save()

def criar_novo_agenda_forn(request):

    dthr = request.POST.get('dado_dthr')
    stsforn = request.POST.get('dado_stscli')
    tpforn = request.POST.get('dado_tpcli')
    usr = User.objects.get(pk = request.POST.get('id_usuario_cred'))
    forn = TBFORN.objects.get(pk = request.POST.get('id_fornecedor_rel'))
    resp = request.POST.get('dado_resp')
    ass = request.POST.get('dado_ass')
    dsc = request.POST.get('dado_dsc')

    agendaforn = TBAGENDAFORN(
        dthr = dthr,
        stsagendaforn = stsforn,
        tipocontatoforn = tpforn,
        fk_user = usr,
        fk_tbforn = forn,
        resp = resp,
        assunto = ass,
        dsc = dsc,
    )
    agendaforn.save()

def editar_agenda_cliente_existente(request):

    agendacli = TBAGENDACLI.objects.get(id = request.POST.get('id_agenda'))

    dthr = request.POST.get('dado_dthr')
    stscli = request.POST.get('dado_stscli')
    tpcli = request.POST.get('dado_tpcli')
    usr = User.objects.get(pk = request.POST.get('id_usuario'))
    cli = TBCLI.objects.get(pk = request.POST.get('id_cliente'))
    resp = request.POST.get('dado_resp')
    ass = request.POST.get('dado_ass')
    dsc = request.POST.get('dado_dsc')

    agendacli.dthr = dthr
    agendacli.stsagendacli = stscli
    agendacli.tipocontatocli = tpcli
    agendacli.fk_user = usr
    agendacli.fk_tbcli = cli
    agendacli.resp = resp
    agendacli.assunto = ass
    agendacli.dsc = dsc

    agendacli.save()

def editar_agenda_forn_existente(request):

    agendaforn = TBAGENDAFORN.objects.get(id = request.POST.get('id_agenda'))

    dthr = request.POST.get('dado_dthr')
    stsforn = request.POST.get('dado_stsforn')
    tpforn = request.POST.get('dado_tpforn')
    usr = User.objects.get(pk = request.POST.get('id_usuario'))
    forn = TBFORN.objects.get(pk = request.POST.get('id_fornecedor'))
    resp = request.POST.get('dado_resp')
    ass = request.POST.get('dado_ass')
    dsc = request.POST.get('dado_dsc')

    agendaforn.dthr = dthr
    agendaforn.stsagendaforn = stsforn
    agendaforn.tipocontatoforn = tpforn
    agendaforn.fk_user = usr
    agendaforn.fk_tbforn = forn
    agendaforn.resp = resp
    agendaforn.assunto = ass
    agendaforn.dsc = dsc

    agendaforn.save()

def editar_cliente_existente(request):

    cliente = TBCLI.objects.get(id = request.POST.get('id_cliente'))

    dsc = request.POST.get('dado_dsc')
    tipocli = request.POST.get('dado_tipocli')
    doc = request.POST.get('dado_doc')
    rg = request.POST.get('dado_rg')
    dtnasc = request.POST.get('dado_dtnasc')
    email = request.POST.get('dado_email')
    tel1 = request.POST.get('dado_tel1')
    tel2 = request.POST.get('dado_tel2')
    telrec = request.POST.get('dado_telrec')
    teltrab = request.POST.get('dado_teltrab')
    celular = request.POST.get('dado_celular')
    contato = request.POST.get('dado_contato')
    localtrab = request.POST.get('dado_localtrab')
    dttrab = request.POST.get('dado_dttrab')
    bairro = request.POST.get('dado_bairro')
    num = request.POST.get('dado_num')
    estado = request.POST.get('dado_estado')
    cidade = request.POST.get('dado_cidade')
    rua = request.POST.get('dado_rua')
    ref1 = request.POST.get('dado_ref1')
    ref2 = request.POST.get('dado_ref2')
    ref3 = request.POST.get('dado_ref3')
    obs = request.POST.get('dado_obs')

    cliente.dsc = dsc
    cliente.tipocli = tipocli
    cliente.doc = doc
    cliente.rg = rg
    cliente.dtnasc = dtnasc if dtnasc else cliente.dtnasc
    cliente.email = email
    cliente.tel1 = tel1
    cliente.tel2 = tel2
    cliente.telrec = telrec
    cliente.teltrab = teltrab
    cliente.celular = celular
    cliente.contato = contato
    cliente.localtrab = localtrab
    cliente.dttrab = dttrab if dttrab else cliente.dttrab
    cliente.bairro = bairro
    cliente.num = num
    cliente.estado = estado
    cliente.cidade = cidade
    cliente.rua = rua
    cliente.ref1 = ref1
    cliente.ref2 = ref2
    cliente.ref3 = ref3
    cliente.obs = obs

    if 'dado_img' in request.FILES:
        img = request.FILES['dado_img']
        img.name = f'{cliente.pk}.png'
        cliente.img = img

    cliente.save()

def alterar_limite(request):

    cliente = TBCLI.objects.get(pk = request.POST.get('id_cliente'))

    limite_atual = Decimal(request.POST.get('dado_limite'))
    new_limite = Decimal(request.POST.get('dado_new_limite'))

    cliente.limite = new_limite
    cliente.creddisp = new_limite - (limite_atual - cliente.creddisp)
    cliente.consdisp = new_limite - (limite_atual - cliente.consdisp)
    cliente.save()

def travar_cliente(request):

    cliente = TBCLI.objects.get(pk = request.POST.get('id_cliente'))
    cliente.clientetrav = True
    cliente.save()

def destravar_cliente(request):

    cliente = TBCLI.objects.get(pk = request.POST.get('id_cliente'))
    cliente.clientetrav = False
    cliente.save()

def criar_novo_fornecedor(request):

    razao = request.POST.get('dado_razao')
    doc = request.POST.get('dado_doc')
    tel = request.POST.get('dado_tel')
    email = request.POST.get('dado_email')
    estado = request.POST.get('dado_estado')
    cidade = request.POST.get('dado_cidade')
    bairro = request.POST.get('dado_bairro')
    num = request.POST.get('dado_num')
    rua = request.POST.get('dado_rua')

    parceiro = TBFORN(
        razao = razao,
        doc = doc,
        tel = tel,
        email = email,
        estado = estado,
        cidade = cidade,
        bairro = bairro,
        num = num, 
        rua = rua,
    )
    parceiro.save()

def editar_fornecedor_existente(request):

    forn = TBFORN.objects.get(pk = request.POST.get('id_forn'))

    razao = request.POST.get('dado_razao')
    doc = request.POST.get('dado_doc')
    tel = request.POST.get('dado_tel')
    email = request.POST.get('dado_email')
    estado = request.POST.get('dado_estado')
    cidade = request.POST.get('dado_cidade')
    bairro = request.POST.get('dado_bairro')
    num = request.POST.get('dado_num')
    rua = request.POST.get('dado_rua')

    forn.razao = razao
    forn.doc = doc
    forn.tel = tel
    forn.email = email
    forn.estado = estado
    forn.cidade = cidade
    forn.bairro = bairro
    forn.num = num
    forn.rua = rua

    forn.save()