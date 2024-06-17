from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import *
from django.http import JsonResponse
from django.shortcuts import redirect
from .methods import *
from cfg.models import CTBCATPROD, CTBJURO, CTBITIPOPG
from django.db.models import F
from datetime import datetime, timedelta
from financeiro.models import TBIOCX, STBOTPROD, TBTPROD, TBIOTPROD
from financeiro.lists import Lists as lists_fin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

@method_decorator(permission_required('estoque.view_produtos'), name = 'dispatch')
class SCListProduto(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_produto/sc_list_produto.html'
    model = TBPROD
    paginate_by = 25
    ordering = ['-pk']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['categorias'] = CTBCATPROD.objects.all()
        if any([
            self.request.GET.get('search_id'), 
            self.request.GET.get('search_desc'),
            self.request.GET.get('search_cat'),
            self.request.GET.get('search_tam'),
            self.request.GET.get('search_precoinicio'),
            self.request.GET.get('search_precofim'),
            self.request.GET.get('search_estoque'),
            self.request.GET.get('search_min'),
        ]):
            context['filtrado'] = True
        return context
    
    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset()

        search_id = self.request.GET.get('search_id', '')
        search_desc = self.request.GET.get('search_desc', '')
        search_cat = self.request.GET.get('search_cat', '')
        search_tam = self.request.GET.get('search_tam', '')
        search_precoinicio = self.request.GET.get('search_precoinicio', '')
        search_precofim = self.request.GET.get('search_precofim', '')
        search_estoque = self.request.GET.get('search_estoque', '')
        search_min = self.request.GET.get('search_min', '')
        ordering = self.request.GET.get('ordering')

        if search_id:
            queryset = queryset.filter(id = search_id)
        if search_desc:
            queryset = queryset.filter(dsc__icontains = search_desc)
        if search_cat:
            queryset = queryset.filter(fk_ctbcatprod__dsc__icontains = search_cat)
        if search_tam:
            queryset = queryset.filter(tam__icontains = search_tam)
        if search_precoinicio:
            queryset = queryset.filter(dvlrvenda__gte = search_precoinicio)
        if search_precofim:
            queryset = queryset.filter(dvlrvenda__lte = search_precofim)
        if search_estoque:
            queryset = queryset.filter(qtdestoque__gt = 0)
        if search_min:
            queryset = queryset.filter(qtdestoque__lt = F('qtdmin'))
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

def new_produto(request):

    if request.method == 'POST':
            
        try:

            criar_novo_produto(request)

            return JsonResponse({'concluido': True, 'success': 'Produto cadastrado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_produto'))
    
def edit_produto(request):

    if request.method == 'POST':
            
        try:

            editar_produto_existente(request)

            return JsonResponse({'concluido': True, 'success': 'Produto atualizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_produto'))
    
def edit_preco(request):

    if request.method == 'POST':
            
        try:

            editar_preco_de_venda(request)

            return JsonResponse({'concluido': True, 'success': 'Preço de venda atualizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_produto'))
    
def altera_custo(request):

    if request.method == 'POST':
            
        try:
            print('aqui')
            change_custo(request)

            return JsonResponse({'concluido': True, 'success': 'Custo atualizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_produto'))

def relatorio_estoque(request):

    if request.method == 'POST':
            
        try:

            error = gerar_relatorio_estoque()

            if error == '':

                return JsonResponse({'concluido': True, 'pdf_path': os.path.join(settings.MEDIA_URL, 'pdf/relatorio_estoque.pdf')})
            
            else:

                return JsonResponse({'concluido': False, 'erros': {'__all__': [error]}})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_produto'))
    
def relatorio_consignado(request):

    if request.method == 'POST':
            
        try:

            error = gerar_relatorio_consignado()

            if error == '':

                return JsonResponse({'concluido': True, 'pdf_path': os.path.join(settings.MEDIA_URL, 'pdf/relatorio_consignado.pdf')})
            
            else:

                return JsonResponse({'concluido': False, 'erros': {'__all__': [error]}})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_produto'))
    
@method_decorator(permission_required('estoque.view_etiquetas'), name = 'dispatch')
class SCInsertEtiqueta(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_insert_etiqueta/sc_insert_etiqueta.html'
    model = STBPPROD

    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset().filter(fk_user = self.request.user)
        return queryset

def new_etiqueta(request):

    if request.method == 'POST':
            
        try:

            criar_nova_etiqueta(request)

            return JsonResponse({'concluido': True, 'success': 'Produto adicionado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_etiqueta'))
    
def delete_etiqueta(request):

    if request.method == 'POST':
            
        try:

            excluir_etiqueta(request)

            return JsonResponse({'concluido': True, 'success': 'Produto removido da lista!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_etiqueta'))
    
def clear_etiqueta(request):

    if request.method == 'POST':
            
        try:

            limpar_etiquetas(request)

            return JsonResponse({'concluido': True, 'success': 'Produtos removidos da lista!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_etiqueta'))
    
def confirm_etiqueta(request):

    if request.method == 'POST':
            
        try:

            imagens = gerar_etiquetas(request)
            gerar_pdf(imagens)
            excluir_imagens_de_media()
            limpar_etiquetas(request)

            return JsonResponse({'concluido': True, 'pdf_path': os.path.join(settings.MEDIA_URL, 'pdf/etiquetas.pdf')})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_etiqueta'))

@method_decorator(permission_required('estoque.view_inventarios'), name = 'dispatch')
class SCInsertInventario(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_insert_inventario/sc_insert_inventario.html'
    model = STBIINV
    paginate_by = 25

    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset().filter(fk_user = self.request.user)
        return queryset
    
def new_inventario(request):

    if request.method == 'POST':
            
        try:

            criar_nova_lista_de_inventario(request)

            return JsonResponse({'concluido': True, 'success': 'Produto adicionado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})
        
        except TBPROD.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Produto não encontrado!']}})

    else:
        return redirect(reverse_lazy('sc_insert_inventario'))
    
def delete_inventario(request):

    if request.method == 'POST':
            
        try:

            excluir_produto_da_lista_do_inventario(request)

            return JsonResponse({'concluido': True, 'success': 'Produto removido da lista!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_inventario'))
    
def clear_inventario(request):

    if request.method == 'POST':
            
        try:

            limpar_inventario(request)

            return JsonResponse({'concluido': True, 'success': 'Produtos removidos da lista!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_inventario'))
    
def confirm_inventario(request):

    if request.method == 'POST':
            
        try:

            inventario = criar_novo_inventario(request)
            gerar_diferencas(request, inventario)
            ajustar_estoque(request, inventario)
            limpar_inventario(request)

            redirect_url = reverse('sc_list_inventario') + '?success=Inventário+gerado+e+estoque+ajustado!'
            return JsonResponse({'concluido': True, 'redirect_url': redirect_url})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_inventario'))

@method_decorator(permission_required('estoque.view_inventarios'), name = 'dispatch')
class SCListInventario(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_inventario/sc_list_inventario.html'
    model = TBINV
    paginate_by = 25
    ordering = ['-pk']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        inventarios_na_pagina = context['object_list']
        inventarios_na_pagina = [inv for inv in inventarios_na_pagina]
        context['diferencas'] = TBDIFINV.objects.filter(fk_tbinv__in = inventarios_na_pagina)
        if self.request.GET.get('search_user'):
            user = User.objects.filter(pk = self.request.GET.get('search_user'))
            context['usuario'] = f'{user[0].first_name} {user[0].last_name}' if user else None
        if any([
            self.request.GET.get('search_user'), 
            self.request.GET.get('search_dtinicio'),
            self.request.GET.get('search_dtfim')
        ]):
            context['filtrado'] = True
        return context

    def get_queryset(self) -> QuerySet[Any]:
        
        queryset = super().get_queryset()

        search_user = self.request.GET.get('search_user', '')
        search_dtinicio = self.request.GET.get('search_dtinicio', '')
        search_dtfim = self.request.GET.get('search_dtfim', '')
        ordering = self.request.GET.get('ordering')

        if search_user:
            queryset = queryset.filter(fk_user__pk = search_user)
        if search_dtinicio:
            queryset = queryset.filter(dt__gte = search_dtinicio)
        if search_dtfim:
            dtfim_datetime = datetime.strptime(search_dtfim, '%Y-%m-%d')
            dtfim_endofday = dtfim_datetime + timedelta(days = 1) - timedelta(microseconds = 1)
            queryset = queryset.filter(dt__lte = dtfim_endofday)
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset

@method_decorator(permission_required('estoque.view_consignado'), name = 'dispatch')  
class SCListConsignado(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_consignado/sc_list_consignado.html'
    model = TBCSG
    paginate_by = 25
    ordering = ['-pk']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        consignados_na_pagina = context['object_list']
        consignados_na_pagina = [cons for cons in consignados_na_pagina]
        context['produtos'] = TBIOCSG.objects.filter(fk_tbcsg__in = consignados_na_pagina)
        context['status'] = Lists.list_status_consignado
        if self.request.GET.get('search_cli'):
            cli = TBCLI.objects.filter(pk = self.request.GET.get('search_cli'))
            context['cliente'] = cli[0] if cli else None
        if self.request.GET.get('search_func'):
            func = User.objects.filter(pk = self.request.GET.get('search_func'))
            context['funcionario'] = f'{func[0].first_name} {func[0].last_name}' if func else None
        if any([
            self.request.GET.get('search_cli'), 
            self.request.GET.get('search_func'),
            self.request.GET.get('search_retiradainicio'),
            self.request.GET.get('search_retiradafim'),
            self.request.GET.get('search_devinicio'),
            self.request.GET.get('search_devfim'),
            self.request.GET.get('search_status'),
        ]):
            context['filtrado'] = True
        return context

    def get_queryset(self) -> QuerySet[Any]:
        
        queryset = super().get_queryset()

        search_cli = self.request.GET.get('search_cli', '')
        search_func = self.request.GET.get('search_func', '')
        search_retiradainicio = self.request.GET.get('search_retiradainicio', '')
        search_retiradafim = self.request.GET.get('search_retiradafim', '')
        search_devinicio = self.request.GET.get('search_devinicio', '')
        search_devfim = self.request.GET.get('search_devfim', '')
        search_status = self.request.GET.get('search_status', '')
        ordering = self.request.GET.get('ordering')

        if search_cli:
            queryset = queryset.filter(fk_tbcli__pk = search_cli)
        if search_func:
            queryset = queryset.filter(fk_user__pk = search_func)
        if search_retiradainicio:
            queryset = queryset.filter(dtinicio__gte = search_retiradainicio)
        if search_retiradafim:
            dtfim_datetime = datetime.strptime(search_retiradafim, '%Y-%m-%d')
            dtfim_endofday = dtfim_datetime + timedelta(days = 1) - timedelta(microseconds = 1)
            queryset = queryset.filter(dtinicio__lte = dtfim_endofday)
        if search_devinicio:
            queryset = queryset.filter(dtfim__gte = search_devinicio)
        if search_devfim:
            dtfim_datetime = datetime.strptime(search_devfim, '%Y-%m-%d')
            dtfim_endofday = dtfim_datetime + timedelta(days = 1) - timedelta(microseconds = 1)
            queryset = queryset.filter(dtfim__lte = dtfim_endofday)
        if search_status:
            queryset = queryset.filter(sts = search_status)
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset

@method_decorator(permission_required('estoque.view_consignado'), name = 'dispatch')    
class SCInsertConsignado(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_insert_consignado/sc_insert_consignado.html'
    model = STBOCSG

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['fk'] = self.kwargs['fk']
        context['caixa'] = TBIOCX.objects.latest('pk')
        consignados = STBOCSG.objects.filter(fk_tbcsg = self.kwargs['fk'], sel = True)
        total = sum(consignado.dvlrtotal for consignado in consignados)
        context['total'] = total
        context['consignado'] = TBCSG.objects.filter(pk = self.kwargs['fk'])
        context['tipopg'] = CTBITIPOPG.objects.all()
        context['juros'] = CTBJURO.objects.all()
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(fk_tbcsg = self.kwargs['fk'], sel = True)
    
def devolucao_consignado(request):

    if request.method == 'POST':
            
        try:

            devolver_consignado(request)

            return JsonResponse({'concluido': True, 'success': 'Produto devolvido!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))

@method_decorator(permission_required('estoque.view_troca'), name = 'dispatch')
class SCListTroca(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_troca/sc_list_troca.html'
    model = TBTPROD
    paginate_by = 25
    ordering = ['-pk']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        trocas_na_pagina = context['object_list']
        trocas_na_pagina = [troca for troca in trocas_na_pagina]
        context['produtos'] = TBIOTPROD.objects.filter(fk_tbtprod__in = trocas_na_pagina)
        selected = [lists_fin.list_status_troca[i] for i in [0, 1]]
        context['status'] = selected
        if self.request.GET.get('search_cli'):
            cli = TBCLI.objects.filter(pk = self.request.GET.get('search_cli'))
            context['cliente'] = cli[0] if cli else None
        if any([
            self.request.GET.get('search_cli'),
            self.request.GET.get('search_dtinicio'),
            self.request.GET.get('search_dtfim'),
            self.request.GET.get('search_status'),
        ]):
            context['filtrado'] = True
        return context

    def get_queryset(self) -> QuerySet[Any]:
        
        queryset = super().get_queryset()

        search_cli = self.request.GET.get('search_cli', '')
        search_dtinicio = self.request.GET.get('search_dtinicio', '')
        search_dtfim = self.request.GET.get('search_dtfim', '')
        search_status = self.request.GET.get('search_status', '')
        ordering = self.request.GET.get('ordering')

        if search_cli:
            queryset = queryset.filter(fk_tbcli__pk = search_cli)
        if search_dtinicio:
            queryset = queryset.filter(dt__gte = search_dtinicio)
        if search_dtfim:
            dtfim_datetime = datetime.strptime(search_dtfim, '%Y-%m-%d')
            dtfim_endofday = dtfim_datetime + timedelta(days = 1) - timedelta(microseconds = 1)
            queryset = queryset.filter(dt__lte = dtfim_endofday)
        if search_status:
            queryset = queryset.filter(sts = search_status)
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset

@method_decorator(permission_required('financeiro.view_troca'), name = 'dispatch')
class SCInsertTroca(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_insert_troca/sc_insert_troca.html'
    model = STBOTPROD

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['fk'] = self.kwargs['fk']
        context['caixa'] = TBIOCX.objects.latest('pk')
        trocas = STBOTPROD.objects.filter(fk_tbtprod = self.kwargs['fk'])
        pre_valor = sum(i.dvlr * i.qtd for i in TBIOTPROD.objects.filter(fk_tbtprod = self.kwargs['fk']))
        total = sum(troca.dvlrtotal for troca in trocas) - pre_valor
        context['total'] = total
        context['troca'] = TBTPROD.objects.filter(pk = self.kwargs['fk'])
        context['tipopg'] = CTBITIPOPG.objects.all()
        context['juros'] = CTBJURO.objects.all()
        return context