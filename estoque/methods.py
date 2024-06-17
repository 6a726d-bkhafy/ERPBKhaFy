from .models import *
from cfg.models import CTBCATPROD
from decimal import Decimal, ROUND_DOWN
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageFont, ImageDraw
import os
import shutil
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import white
from reportlab.platypus import Image as img_canvas
from datetime import datetime
from django.db.models.query import Q
from index.pdf_creator.create_table_fpdf2 import PDF

def criar_novo_produto(request):

    desc = request.POST.get('dado_desc')
    tam = request.POST.get('dado_tam')
    categoria = CTBCATPROD.objects.get(pk = request.POST.get('id_categoria'))
    qtdmin = request.POST.get('dado_min')
    pvlrmmin = request.POST.get('dado_margem')
    ncm = request.POST.get('dado_ncm')

    produto = TBPROD(
        dsc = desc,
        tam = tam,
        fk_ctbcatprod = categoria,
        qtdmin = qtdmin,
        pvlrmmin = pvlrmmin,
        ncm = ncm
    )

    produto.save()

    if 'dado_img' in request.FILES:
        img = request.FILES['dado_img']
        img.name = f'{produto.pk}.png'
        produto.img = img
        produto.save()

def editar_produto_existente(request):

    produto = TBPROD.objects.get(pk = request.POST.get('id_produto'))

    desc = request.POST.get('dado_desc')
    tam = request.POST.get('dado_tam')
    categoria = CTBCATPROD.objects.get(pk = request.POST.get('id_categoria'))
    qtdmin = request.POST.get('dado_min')
    pvlrmmin = request.POST.get('dado_margem')
    ncm = request.POST.get('dado_ncm')

    produto.dsc = desc
    produto.tam = tam
    produto.fk_ctbcatprod = categoria
    produto.qtdmin = qtdmin
    produto.pvlrmmin = pvlrmmin
    produto.ncm = ncm

    if 'dado_img' in request.FILES:
        img = request.FILES['dado_img']
        img.name = f'{produto.pk}.png'
        produto.img = img

    produto.save()

def editar_preco_de_venda(request):

    valor = Decimal(request.POST.get('dado_valor'))
    produto = TBPROD.objects.get(pk = request.POST.get('id_produto'))

    valor = Decimal(request.POST.get('dado_valor'))
    produto = TBPROD.objects.get(pk=request.POST.get('id_produto'))

    if produto.dvlrcusto > 0:
        margem = valor / produto.dvlrcusto
        porcentagem = 100 * (margem - 1)
    else:
        porcentagem = 0

    max_value = Decimal('9999999999.99')  # Um pouco menos de 10 dígitos no total
    porcentagem = Decimal(porcentagem).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    porcentagem = min(porcentagem, max_value)
    produto.dvlrvenda = valor
    produto.pvlrmatual = porcentagem
    produto.save()

def change_custo(request):

    custo = Decimal(request.POST.get('dado_custo'))
    produto = TBPROD.objects.get(pk = request.POST.get('id_produto'))

    produto.dvlrcusto = custo
    print(custo)
    produto.save()

def criar_nova_etiqueta(request):

    produto = TBPROD.objects.get(pk = request.POST.get('id_produto'))
    qtd = Decimal(request.POST.get('dado_qtd'))

    etiqueta = STBPPROD.objects.filter(fk_tbprod = produto, fk_user = request.user)

    if etiqueta:

        etiqueta[0].qtd += qtd
        etiqueta[0].save()

    else:

        etiqueta = STBPPROD(
            fk_tbprod = produto,
            qtd = qtd,
            fk_user = request.user
        )
        etiqueta.save()

def excluir_etiqueta(request):

    etiqueta = STBPPROD.objects.get(pk = request.POST.get('id_etiqueta'))
    etiqueta.delete()

def limpar_etiquetas(request):

    etiquetas = STBPPROD.objects.filter(fk_user = request.user)
    etiquetas.delete()

def gerar_etiquetas(request):

    etiquetas = STBPPROD.objects.filter(fk_user = request.user)

    imagens = []

    for etiqueta in etiquetas:

        for et in range(etiqueta.qtd):

            et += 1

            barcode_path = os.path.join(settings.MEDIA_ROOT, f'img/codigo_{etiqueta.fk_tbprod.pk}')
            codigo = Code128(str(etiqueta.fk_tbprod.pk).zfill(6), writer=ImageWriter())
            codigo.save(barcode_path)

            imagem1 = Image.open(f'{barcode_path}.png')

            width, height = imagem1.size
            new_width = int(width * 2)
            imagem1 = imagem1.resize((new_width, height), Image.LANCZOS)

            logo_path = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
            imagem2 = Image.open(logo_path)

            imagem1 = imagem1.rotate(90, expand=True)

            largura1, altura1 = imagem1.size
            largura2, altura2 = imagem2.size

            largura_logo = 300
            altura_logo = int(imagem2.height * (largura_logo / imagem2.width))
            imagem2 = imagem2.resize((largura_logo, altura_logo))

            largura_total = largura1 + largura2

            nova_imagem = Image.new('RGB', (largura_total, max(altura1, altura2) + 50), (255, 255, 255))

            nova_imagem.paste(imagem1, (largura2, 0))

            draw = ImageDraw.Draw(nova_imagem)

            font_path = os.path.join(settings.STATIC_ROOT, "font/Roboto-Black.ttf")
            font = ImageFont.truetype(font_path, 100)

            offset_esquerda = 100

            texto_preco = f"R$ {etiqueta.fk_tbprod.dvlrvenda}"
            posicao_preco = (int(largura_total / 2) - offset_esquerda, max(altura1, altura2) - 300)

            draw.text(posicao_preco, texto_preco, fill=(0, 0, 0), font=font, anchor='mm')

            font_path = os.path.join(settings.STATIC_ROOT, "font/Roboto-Black.ttf")
            font = ImageFont.truetype(font_path, 50)
            texto_produto = f"{etiqueta.fk_tbprod.dsc}"

            if len(texto_produto) >= 20:
                meio = len(texto_produto) // 2
                texto_produto = texto_produto[:meio] + '\n' + texto_produto[meio:]

            x_central = int(largura_total / 2)
            y_inicial = max(altura1, altura2) - 150

            linhas = texto_produto.split('\n')
            altura_linha = 50

            for i, linha in enumerate(reversed(linhas)):
                y = y_inicial - i * altura_linha
                draw.text((x_central - offset_esquerda, y), linha, fill=(0, 0, 0), font=font, anchor='mm')

            new_image_path = os.path.join(settings.MEDIA_ROOT, f'img/etiqueta_{etiqueta.fk_tbprod.pk}_{et}.png')
            nova_imagem.save(new_image_path)

            imagens.append(new_image_path)

    return imagens

def gerar_pdf(imagens):
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdf/etiquetas.pdf')

    c = Canvas(pdf_path, pagesize=A4)
    c.setTitle('Etiquetas')

    num_linhas = 9
    num_colunas = 3
    imagens_por_pagina = num_linhas * num_colunas 

    largura_celula = A4[0] / num_colunas
    altura_celula = A4[1] / num_linhas

    imagens_adicionadas = 0  

    for imagem_path in imagens:
        
        if imagens_adicionadas % imagens_por_pagina == 0:
            c.setStrokeColor(white)

            for i in range(1, num_linhas):
                y = i * altura_celula
                c.line(0, y, A4[0], y)
            for i in range(1, num_colunas):
                x = i * largura_celula
                c.line(x, 0, x, A4[1])
            if imagens_adicionadas != 0:
                c.showPage()

        i = (imagens_adicionadas % imagens_por_pagina) // num_colunas
        j = (imagens_adicionadas % imagens_por_pagina) % num_colunas

        x1 = j * largura_celula
        x2 = (j + 1) * largura_celula
        y1 = (num_linhas - i - 1) * altura_celula
        y2 = (num_linhas - i) * altura_celula

        imagem = img_canvas(imagem_path, width=x2 - x1, height=y2 - y1)
        imagem.drawOn(c, x1, y1)

        imagens_adicionadas += 1

    c.showPage()
    c.save()

def excluir_imagens_de_media():

    img_directory = os.path.join(settings.MEDIA_ROOT, 'img')
    for filename in os.listdir(img_directory):
        file_path = os.path.join(img_directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Falha ao excluir {file_path}. Razão: {e}')

def criar_nova_lista_de_inventario(request):

    produto = TBPROD.objects.get(pk = request.POST.get('id_produto'))

    inventario = STBIINV.objects.filter(fk_tbprod = produto, fk_user = request.user)

    if inventario:

        inventario[0].qtdcont += 1
        inventario[0].save()

    else:

        inventario = STBIINV(
            fk_tbprod = produto,
            qtdcont = 1,
            fk_user = request.user
        )
        inventario.save()

def excluir_produto_da_lista_do_inventario(request):

    inventario = STBIINV.objects.get(pk = request.POST.get('id_inventario'))
    inventario.delete()

def limpar_inventario(request):

    inventarios = STBIINV.objects.filter(fk_user = request.user)
    inventarios.delete()

def criar_novo_inventario(request):

    inventario = TBINV(
        dt = datetime.now(),
        fk_user = request.user
    )
    inventario.save()

    return inventario

def gerar_diferencas(request, inventario):

    lista_inventario = STBIINV.objects.filter(fk_user = request.user)
    com_estoque = [i.fk_tbprod.pk for i in lista_inventario]
    sem_estoque = TBPROD.objects.filter(Q(qtdestoque__gt = 0) & ~Q(pk__in = com_estoque))

    diferencas = []

    for inv in lista_inventario:

        if inv.qtdcont != inv.fk_tbprod.qtdestoque:

            diferenca = TBDIFINV(
                fk_tbprod = inv.fk_tbprod,
                fk_tbinv = inventario,
                qtdcont = inv.qtdcont,
                qtdestoque = inv.fk_tbprod.qtdestoque,
                dif = inv.qtdcont - inv.fk_tbprod.qtdestoque
            )
            diferencas.append(diferenca)

    for prod in sem_estoque:
        
        diferenca = TBDIFINV(
            fk_tbprod = prod,
            fk_tbinv = inventario,
            qtdcont = 0,
            qtdestoque = prod.qtdestoque,
            dif = 0 - prod.qtdestoque
        )
        diferencas.append(diferenca)

    TBDIFINV.objects.bulk_create(diferencas)

def ajustar_estoque(request, inventario):

    diferencas_dict = {dif.fk_tbprod: dif.dif for dif in TBDIFINV.objects.filter(fk_tbinv = inventario)}
    produtos_sem_diferenca = [inv.fk_tbprod for inv in STBIINV.objects.filter(fk_user = request.user)]
    produtos_com_estoque_positivo = TBPROD.objects.filter(qtdestoque__gt = 0)
    produtos_para_zero = [prod.pk for prod in produtos_com_estoque_positivo if prod not in diferencas_dict and prod not in produtos_sem_diferenca]

    TBPROD.objects.filter(pk__in = produtos_para_zero).update(qtdestoque = 0)

    for prod, dif in diferencas_dict.items():

        prod.qtdestoque += dif
        prod.save()

def devolver_consignado(request):

    consignado = TBCSG.objects.get(pk = request.POST.get('id_consignado'))
    consignados = TBIOCSG.objects.filter(fk_tbcsg = consignado, sts = '0')

    cliente = consignado.fk_tbcli

    for cons in consignados:

        qtd = int(request.POST.get(f'dado_{cons.pk}')) if request.POST.get(f'dado_{cons.pk}') else 0

        cons.qtd -= qtd
        cons_venda = STBOCSG.objects.get(fk_tbprod = cons.fk_tbprod, estoque = cons.estoque, fk_tbcsg = cons.fk_tbcsg)
        cons_venda.qtd -= qtd

        dev = TBIOCSG.objects.filter(fk_tbprod = cons.fk_tbprod, sts = '2', fk_tbcsg = consignado)

        cliente.consdisp += cons_venda.dvlrund * qtd
        cliente.save()

        if dev:
            dev[0].qtd += qtd
            dev[0].save()
        elif qtd != 0:
            dev = TBIOCSG(
                fk_tbprod = cons.fk_tbprod,
                fk_tbcsg = consignado,
                qtd = qtd,
                sts = '2',
                estoque = cons.estoque
            ) 
            dev.save()

        produto = cons.fk_tbprod
        produto.qtdcsg -= qtd
        produto.save()

        cons.save() if cons.qtd > 0 else cons.delete()
        cons_venda.save() if cons_venda.qtd > 0 else cons_venda.delete()

    total_em_consignado = sum(cons.qtd for cons in consignados)

    if total_em_consignado == 0:

        consignado.sts = '2'

    elif total_em_consignado < consignado.qtd:

        consignado.sts = '1'

    consignado.save()

def gerar_relatorio_estoque():

    error = ''

    object = TBPROD.objects.filter(qtdestoque__gt = 0)

    if not object:

        error = 'O filtro escolhido não retornou dados!'

    else:

        pdf = PDF()
        pdf.set_font("Times", size=10)
        pdf.set_landscape()

        total = sum(i.dvlrvenda for i in object)

        data = [['Código', 'Descrição', 'Categoria', 'Tamanho', 'Estoque', 'Preço de Venda']]

        cont = 0
        total_linhas = object.count()

        for obj in object:

            cont += 1

            linha = [
                f'{obj.pk}',
                f'{obj.dsc}', 
                f'{obj.fk_ctbcatprod.dsc}', 
                f'{obj.tam}', 
                f'{obj.qtdestoque}',
                f'R$ {obj.dvlrvenda}'
            ]

            data.append(linha)

            if cont == 17:

                total_linhas -= cont
                cont = 0
        
                pdf.create_table(table_data = data, title = 'SAVANA STORE', subtitle = 'Relatório de Estoque', align_header = 'C', align_data = 'C', cell_width = 'even')
                
                data = [['Código', 'Valor Total', 'Vendedor', 'Cliente', 'Tipo de Pagamento', 'Data']]

            if cont == total_linhas:

                pdf.create_table(table_data = data, title = 'SAVANA STORE', subtitle = 'Relatório de Estoque', align_header = 'C', align_data = 'C', cell_width = 'even')

        pdf.cell(270, 10, txt=f"Total: R$ {total}", ln=True, align='R')

        path = os.path.join(settings.MEDIA_ROOT, f'pdf/relatorio_estoque.pdf')

        pdf.output(path)

    return error

def gerar_relatorio_consignado():

    error = ''

    object = TBPROD.objects.filter(qtdcsg__gt = 0)

    if not object:

        error = 'O filtro escolhido não retornou dados!'

    else:

        pdf = PDF()
        pdf.set_font("Times", size=10)
        pdf.set_landscape()

        total = sum(i.dvlrvenda for i in object)

        data = [['Código', 'Descrição', 'Categoria', 'Tamanho', 'Em Consignado', 'Preço de Venda']]

        cont = 0
        total_linhas = object.count()

        for obj in object:

            cont += 1

            linha = [
                f'{obj.pk}',
                f'{obj.dsc}', 
                f'{obj.fk_ctbcatprod.dsc}', 
                f'{obj.tam}', 
                f'{obj.qtdcsg}',
                f'R$ {obj.dvlrvenda}'
            ]

            data.append(linha)

            if cont == 17:

                total_linhas -= cont
                cont = 0
        
                pdf.create_table(table_data = data, title = 'SAVANA STORE', subtitle = 'Relatório de Consignado', align_header = 'C', align_data = 'C', cell_width = 'even')
                
                data = [['Código', 'Valor Total', 'Vendedor', 'Cliente', 'Tipo de Pagamento', 'Data']]

            if cont == total_linhas:

                pdf.create_table(table_data = data, title = 'SAVANA STORE', subtitle = 'Relatório de Consignado', align_header = 'C', align_data = 'C', cell_width = 'even')

        pdf.cell(270, 10, txt=f"Total: R$ {total}", ln=True, align='R')

        path = os.path.join(settings.MEDIA_ROOT, f'pdf/relatorio_consignado.pdf')

        pdf.output(path)

    return error
