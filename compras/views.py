from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import *
from django.shortcuts import redirect
from django.http import JsonResponse
from .methods import *
from datetime import datetime, timedelta
from cfg.models import CTBCATFIN
import os
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

@method_decorator(permission_required('compras.view_compra'), name = 'dispatch')
class SCListCompra(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_compra.html'
    model = TBCOMP
    paginate_by = 25
    ordering = ['-dt']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['status'] = Lists.list_status
        ordens_na_pagina = context['object_list']
        ordens_na_pagina = [ordem for ordem in ordens_na_pagina]
        context['entradas'] = TBIPROD.objects.filter(fk_tbcomp__in = ordens_na_pagina)
        if any([
            self.request.GET.get('search_forn'),
            self.request.GET.get('search_dtinicio'),
            self.request.GET.get('search_dtfim'),
            self.request.GET.get('search_status'),
        ]):
            context['filtrado'] = True
        if self.request.GET.get('search_forn'):
            forn = TBFORN.objects.filter(pk = self.request.GET.get('search_forn'))
            context['fornecedor'] = forn[0] if forn else None
        return context

    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset()

        search_forn = self.request.GET.get('search_forn', '')
        search_dtinicio = self.request.GET.get('search_dtinicio', '')
        search_dtfim = self.request.GET.get('search_dtfim', '')
        search_status = self.request.GET.get('search_status', '')
        ordering = self.request.GET.get('ordering')

        if search_forn:
            queryset = queryset.filter(fk_tbforn__pk = search_forn)
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

def entrada_compra(request):

    if request.method == 'POST':
            
        try:

            ordem, entradas = realizar_entrada(request)
            validar_status_da_ordem(ordem, entradas)

            return JsonResponse({'concluido': True, 'success': 'Entrada realizada e estoque ajustado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_compra'))

def estorno_compra(request):

    if request.method == 'POST':
            
        try:

            realizar_estorno_de_compra(request)

            return JsonResponse({'concluido': True, 'success': 'Estorno realizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_compra'))
    
def new_etiquetas(request):

    if request.method == 'POST':
            
        try:

            gerar_etiquetas(request)

            redirect_url = reverse('sc_insert_etiqueta') + '?success=Etiquetas+geradas!'
            return JsonResponse({'concluido': True, 'redirect_url': redirect_url})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_compra'))

def relatorio_compra(request):

    if request.method == 'POST':
            
        try:

            error = gerar_relatorio_compra(request)

            if error == '':

                return JsonResponse({'concluido': True, 'pdf_path': os.path.join(settings.MEDIA_URL, 'pdf/relatorio_compra.pdf')})
            
            else:

                return JsonResponse({'concluido': False, 'erros': {'__all__': [error]}})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_compra'))

@method_decorator(permission_required('compras.view_compra'), name = 'dispatch')
class SCInsertCompra(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_insert_compra.html'
    model = STBICOMP

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['custos'] = CTBCATFIN.objects.all()
        context['fk'] = self.kwargs['fk']
        if self.kwargs['fk'] != 0:
            context['ordem'] = TBCOMP.objects.filter(pk = self.kwargs['fk'])
        return context
    
    def get_queryset(self) -> QuerySet[Any]:

        return super().get_queryset().filter(fk_tbcomp = self.kwargs['fk'])

def add_item_compra(request, fk):

    if request.method == 'POST':
            
        try:

            ordem: TBCOMP = criar_nova_ordem(request, fk)
            adicionar_produto_a_lista(request, ordem)

            redirect_url = reverse('sc_insert_compra', args=[ordem.pk]) + '?success=Produto+adicionado!'
            return JsonResponse({'concluido': True, 'redirect_url': redirect_url})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})
        
        except TBFORN.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Parceiro não encontrado!']}})

    else:
        return redirect(reverse_lazy('sc_insert_compra'))

def delete_compra(request):

    if request.method == 'POST':
            
        try:

            excluir_produto_da_lista(request)

            return JsonResponse({'concluido': True, 'success': 'Produto removido da lista!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_compra'))
    
def clear_compra(request, fk):

    if request.method == 'POST':
            
        try:

            excluir_todos_os_produtos_da_lista(fk)

            return JsonResponse({'concluido': True, 'success': 'Produtos removidos da lista!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_compra'))
    
def qtd_compra(request):

    if request.method == 'POST':
            
        try:

            alterar_quantidade_de_um_produto(request)

            return JsonResponse({'concluido': True, 'success': 'Quantidade alterada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_compra'))
    
def confirm_compra(request, fk):

    if request.method == 'POST':
            
        try:

            ordem = criar_entrada_de_produto(fk)
            criar_lancamento_financeiro(ordem)

            redirect_url = reverse('sc_list_compra') + '?success=Ordem+gerada!'
            return JsonResponse({'concluido': True, 'redirect_url': redirect_url})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_compra'))
    

@method_decorator(permission_required('compras.view_lote'), name = 'dispatch')    
class SCListLote(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_lote.html'
    model = TBLOTE
    paginate_by = 25
    ordering = ['-dt']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['status'] = Lists.list_status_lote
        ordens_na_pagina = context['object_list']
        ordens_na_pagina = [ordem for ordem in ordens_na_pagina]
        context['entradas'] = TBILOTE.objects.filter(fk_tblote__in = ordens_na_pagina)
        return context

    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset()

        search_forn = self.request.GET.get('search_forn', '')
        search_dtinicio = self.request.GET.get('search_dtinicio', '')
        search_dtfim = self.request.GET.get('search_dtfim', '')
        search_status = self.request.GET.get('search_status', '')
        ordering = self.request.GET.get('ordering')

        if search_forn:
            queryset = queryset.filter(fk_tbforn__pk = search_forn)
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
    
def entrada_lote(request):

    if request.method == 'POST':
            
        try:

            ordem, entradas = realizar_entrada_lote(request)
            validar_status_do_lote(ordem, entradas)

            return JsonResponse({'concluido': True, 'success': 'Entrada realizada e estoque ajustado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_lote'))

def estorno_lote(request):

    if request.method == 'POST':
            
        try:

            realizar_estorno_de_lote(request)

            return JsonResponse({'concluido': True, 'success': 'Estorno realizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_compra'))
    
@method_decorator(permission_required('compras.view_lote'), name = 'dispatch')    
class SCInsertLote(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_insert_lote.html'
    model = STBILOTE

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['fk'] = self.kwargs['fk']
        if self.kwargs['fk'] != 0:
            context['ordem'] = TBLOTE.objects.filter(pk = self.kwargs['fk'])
        return context
    
    def get_queryset(self) -> QuerySet[Any]:

        return super().get_queryset().filter(fk_tblote = self.kwargs['fk'])

def add_item_lote(request, fk):

    if request.method == 'POST':
            
        try:

            ordem: TBLOTE = criar_nova_ordem_lote(request, fk)
            adicionar_produto_a_lista_lote(request, ordem)

            redirect_url = reverse('sc_insert_lote', args=[ordem.pk]) + '?success=Produto+adicionado!'
            return JsonResponse({'concluido': True, 'redirect_url': redirect_url})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})
        
        except TBFORN.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Parceiro não encontrado!']}})

    else:
        return redirect(reverse_lazy('sc_insert_lote'))

def delete_lote(request):

    if request.method == 'POST':
            
        try:

            excluir_produto_da_lista(request)

            return JsonResponse({'concluido': True, 'success': 'Produto removido da lista!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_compra'))
    
def clear_lote(request, fk):

    if request.method == 'POST':
            
        try:

            excluir_todos_os_produtos_da_lista_lote(fk)

            return JsonResponse({'concluido': True, 'success': 'Produtos removidos da lista!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_compra'))
    
def qtd_lote(request):

    if request.method == 'POST':
            
        try:

            alterar_quantidade_de_um_produto(request)

            return JsonResponse({'concluido': True, 'success': 'Quantidade alterada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_compra'))
    
def confirm_lote(request, fk):

    if request.method == 'POST':
            
        try:
            lt = criar_entrada_de_lote(fk)
            alterar_sts_lote(lt)

            redirect_url = reverse('sc_list_lote') + '?success=Ordem+gerada!'
            return JsonResponse({'concluido': True, 'redirect_url': redirect_url})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_lote'))