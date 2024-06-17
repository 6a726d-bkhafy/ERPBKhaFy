from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet, Q
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from .models import *
from cfg.models import CTBCATFIN, CTBBANK, CTBJURO
from django.http import JsonResponse
from django.shortcuts import redirect
from .methods import *
from .lists import Lists
from datetime import datetime, timedelta
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

@method_decorator(permission_required('financeiro.view_saida'), name = 'dispatch')
class SCListSaidaFinanceiro(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_saida_financeiro/sc_list_saida_financeiro.html'
    model = TBOFIN
    paginate_by = 25
    ordering = ['-pk']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['contas'] = CTBBANK.objects.all()
        context['custos'] = CTBCATFIN.objects.all()
        context['status'] = Lists.list_status
        selected_items = [Lists.list_tipopg[i] for i in [0, 1, 2, 5, 7]]
        context['pagamentos'] = selected_items
        saidas_na_pagina = context['object_list']
        saidas_na_pagina = [sai for sai in saidas_na_pagina]
        pgsaida = TBOPG.objects.filter(fk_tbofin__in = saidas_na_pagina)
        context['pgsaida'] = pgsaida
        context['saidas_com_pagamento'] = [pg.fk_tbofin for pg in pgsaida]
        if self.request.GET.get('search_forn'):
            forn = TBFORN.objects.filter(pk = self.request.GET.get('search_forn'))
            context['fornecedor'] = forn[0] if forn else None
        if any([
            self.request.GET.get('search_numnota'), 
            self.request.GET.get('search_forn'),
            self.request.GET.get('search_eminicio'),
            self.request.GET.get('search_emfim'),
            self.request.GET.get('search_vencinicio'),
            self.request.GET.get('search_vencfim'),
            self.request.GET.get('search_status'),
        ]):
            context['filtrado'] = True
        return context
    
    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset()

        search_numnota = self.request.GET.get('search_numnota', '')
        search_forn = self.request.GET.get('search_forn', '')
        search_eminicio = self.request.GET.get('search_eminicio', '')
        search_emfim = self.request.GET.get('search_emfim', '')
        search_vencinicio = self.request.GET.get('search_vencinicio', '')
        search_vencfim = self.request.GET.get('search_vencfim', '')
        search_status = self.request.GET.get('search_status', '')
        ordering = self.request.GET.get('ordering')

        if search_numnota:
            queryset = queryset.filter(numnota = search_numnota)
        if search_forn:
            queryset = queryset.filter(fk_tbforn__pk = search_forn)
        if search_eminicio:
            queryset = queryset.filter(dtem__gte = search_eminicio)
        if search_emfim:
            dtfim_datetime = datetime.strptime(search_emfim, '%Y-%m-%d')
            dtfim_endofday = dtfim_datetime + timedelta(days = 1) - timedelta(microseconds = 1)
            queryset = queryset.filter(dtem__lte = dtfim_endofday)
        if search_vencinicio:
            queryset = queryset.filter(dtvenc__gte = search_vencinicio)
        if search_vencfim:
            dtfim_datetime = datetime.strptime(search_vencfim, '%Y-%m-%d')
            dtfim_endofday = dtfim_datetime + timedelta(days = 1) - timedelta(microseconds = 1)
        if search_status:
            if search_status == '0':
                queryset = queryset.filter(Q(sts = '0') | Q(sts = '4'))
            else:
                queryset = queryset.filter(sts = search_status)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
    
def new_lancamento(request):

    if request.method == 'POST':
            
        try:

            gerar_lancamento_convencional(request)

            return JsonResponse({'concluido': True, 'success': 'Lançamento gerado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})
        
        except TBCLI.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Cliente não encontrado!']}})
        
        except User.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Vendedor não encontrado!']}})

    else:
        return redirect(reverse_lazy('sc_list_saida_financeiro'))
    
def new_pagamento(request):

    if request.method == 'POST':
            
        try:

            realizar_pagamento(request)

            return JsonResponse({'concluido': True, 'success': 'Pagamento realizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_saida_financeiro'))

def estorno_pagamento_saida(request):

    if request.method == 'POST':
            
        try:

            realizar_estorno_de_pagamento_saida(pg = TBOPG.objects.get(pk = request.POST.get('id_pagamento')))

            return JsonResponse({'concluido': True, 'success': 'Estorno realizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_saida_financeiro'))
    
def new_venc_saida(request):

    if request.method == 'POST':
            
        try:

            alterar_data_de_vencimento_saida(request)

            return JsonResponse({'concluido': True, 'success': 'Data de vencimento alterada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_saida_financeiro'))

def edit_parcelas_saida(request):

    if request.method == 'POST':
            
        try:

            error = alterar_valor_das_parcelas_saida(request)

            if error != '':

                return JsonResponse({'concluido': False, 'erros': {'__all__': [error]}})

            else:

                return JsonResponse({'concluido': True, 'success': 'Valores das parcelas alterados!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_saida_financeiro'))
    
def relatorio_saida(request):

    if request.method == 'POST':
            
        try:

            error = gerar_relatorio_saida(request)

            if error == '':

                return JsonResponse({'concluido': True, 'pdf_path': os.path.join(settings.MEDIA_URL, 'pdf/relatorio_contas_a_pagar.pdf')})
            
            else:

                return JsonResponse({'concluido': False, 'erros': {'__all__': [error]}})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_saida_financeiro'))

@method_decorator(permission_required('financeiro.view_entrada'), name = 'dispatch')
class SCListEntradaFinanceiro(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_entrada_financeiro/sc_list_entrada_financeiro.html'
    model = TBIFIN
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['contas'] = CTBBANK.objects.all()
        context['custos'] = CTBCATFIN.objects.all()
        context['status'] = Lists.list_status
        context['tipopg'] = CTBITIPOPG.objects.all()
        if self.request.GET.get('search_cli'):
            cli = TBCLI.objects.filter(pk = self.request.GET.get('search_cli'))
            context['cliente'] = cli[0] if cli else None
        entradas_na_pagina = context['object_list']
        entradas_na_pagina = [ent for ent in entradas_na_pagina]
        entradas = TBIPG.objects.filter(fk_tbifin__in = entradas_na_pagina)
        context['pgentrada'] = entradas
        context['entradas_com_pagamento'] = [pg.fk_tbifin for pg in entradas]
        crediarios_na_pagina = context['object_list']
        crediarios_na_pagina = [cred.fk_tbicred.pk for cred in crediarios_na_pagina if cred.fk_tbicred]
        context['crediarios'] = TBICRED.objects.filter(pk__in = crediarios_na_pagina)
        
        if any([
            self.request.GET.get('search_numnota'), 
            self.request.GET.get('search_cli'),
            self.request.GET.get('search_eminicio'),
            self.request.GET.get('search_emfim'),
            self.request.GET.get('search_vencinicio'),
            self.request.GET.get('search_vencfim'),
            self.request.GET.get('search_status'),
        ]):
            context['filtrado'] = True
        return context
    
    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset()

        search_numnota = self.request.GET.get('search_numnota', '')
        search_cli = self.request.GET.get('search_cli', '')
        search_eminicio = self.request.GET.get('search_eminicio', '')
        search_emfim = self.request.GET.get('search_emfim', '')
        search_vencinicio = self.request.GET.get('search_vencinicio', '')
        search_vencfim = self.request.GET.get('search_vencfim', '')
        search_status = self.request.GET.get('search_status', '')
        ordering = self.request.GET.get('ordering')

        if search_numnota:
            queryset = queryset.filter(numnota = search_numnota)
        if search_cli:
            queryset = queryset.filter(fk_tbcli__pk = search_cli)
        if search_eminicio:
            queryset = queryset.filter(dtem__gte = search_eminicio)
        if search_emfim:
            dtfim_datetime = datetime.strptime(search_emfim, '%Y-%m-%d')
            dtfim_endofday = dtfim_datetime + timedelta(days = 1) - timedelta(microseconds = 1)
            queryset = queryset.filter(dtem__lte = dtfim_endofday)
        if search_vencinicio:
            queryset = queryset.filter(dtvenc__gte = search_vencinicio)
        if search_vencfim:
            dtfim_datetime = datetime.strptime(search_vencfim, '%Y-%m-%d')
            dtfim_endofday = dtfim_datetime + timedelta(days = 1) - timedelta(microseconds = 1)
            queryset = queryset.filter(dtvenc__lte = dtfim_endofday)
        if search_status:
            if search_status == '0':
                queryset = queryset.filter(Q(sts = '0') | Q(sts = '4'))
            else:
                queryset = queryset.filter(sts = search_status)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

def new_pagamento_entrada_dinheiro(request):

    if request.method == 'POST':
            
        try:

            realizar_pagamento_entrada_dinheiro(request)

            return JsonResponse({'concluido': True, 'success': 'Pagamento realizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_entrada_financeiro'))
    
def new_pagamento_entrada_outros(request):

    if request.method == 'POST':
            
        try:

            realizar_pagamento_entrada_outros(request)

            return JsonResponse({'concluido': True, 'success': 'Pagamento realizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_entrada_financeiro'))
    
def estorno_pagamento_entrada(request):

    if request.method == 'POST':
            
        try:

            realizar_estorno_de_pagamento_entrada(pg = TBIPG.objects.get(pk = request.POST.get('id_pagamento')))

            return JsonResponse({'concluido': True, 'success': 'Estorno realizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_entrada_financeiro'))

def new_venc_entrada(request):

    if request.method == 'POST':
            
        try:

            alterar_data_de_vencimento_entrada(request)

            return JsonResponse({'concluido': True, 'success': 'Data de vencimento alterada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_entrada_financeiro'))
    
def edit_parcelas(request):

    if request.method == 'POST':
            
        try:

            alterar_valor_das_parcelas(request)

            return JsonResponse({'concluido': True, 'success': 'Valores das parcelas alterados!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_entrada_financeiro'))
    
def estorno_lanc(request):

    if request.method == 'POST':
            
        try:

            estornar_lancamento(request)

            return JsonResponse({'concluido': True, 'success': 'Lançamento estornado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_entrada_financeiro'))
    
def relatorio_entrada(request):

    if request.method == 'POST':
            
        try:

            error = gerar_relatorio_entrada(request)

            if error == '':

                return JsonResponse({'concluido': True, 'pdf_path': os.path.join(settings.MEDIA_URL, 'pdf/relatorio_contas_a_receber.pdf')})
            
            else:

                return JsonResponse({'concluido': False, 'erros': {'__all__': [error]}})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_entrada_financeiro'))

@method_decorator(permission_required('financeiro.view_caixa'), name = 'dispatch')
class SCListCaixa(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_caixa/sc_list_caixa.html'
    model = TBCX
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['status'] = Lists.list_status_caixa
        movimentacoes_na_pagina = context['object_list']
        movimentacoes_na_pagina = [mov for mov in movimentacoes_na_pagina]
        pg_dinheiro = [mov for mov in movimentacoes_na_pagina if not mov.fk_ctbitipopg]
        context['caixas_com_pagamento'] = pg_dinheiro
        context['pgcaixa'] = TBIPG.objects.filter(fk_tbcx__in = pg_dinheiro)
        context['produtos'] = TBOPROD.objects.filter(fk_tbcx__in = movimentacoes_na_pagina)
        if self.request.GET.get('search_cli'):
            cli = TBCLI.objects.filter(pk = self.request.GET.get('search_cli'))
            context['cliente'] = cli[0] if cli else None
        if self.request.GET.get('search_func'):
            func = User.objects.filter(pk = self.request.GET.get('search_func'))
            context['funcionario'] = f'{func[0].first_name} {func[0].last_name}' if func else None
        if any([
            self.request.GET.get('search_id'), 
            self.request.GET.get('search_func'),
            self.request.GET.get('search_cli'),
            self.request.GET.get('search_dtinicio'),
            self.request.GET.get('search_dtfim'),
            self.request.GET.get('search_status'),
        ]):
            context['filtrado'] = True
        return context
    
    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset()

        search_id = self.request.GET.get('search_id', '')
        search_func = self.request.GET.get('search_func', '')
        search_cli = self.request.GET.get('search_cli', '')
        search_dtinicio = self.request.GET.get('search_dtinicio', '')
        search_dtfim = self.request.GET.get('search_dtfim', '')
        search_status = self.request.GET.get('search_status', '')
        ordering = self.request.GET.get('ordering')

        if search_id:
            queryset = queryset.filter(pk = search_id)
        if search_func:
            queryset = queryset.filter(fk_user__pk = search_func)
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

def new_troca(request):

    if request.method == 'POST':
            
        try:

            criar_ordem_de_troca(request)

            return JsonResponse({'concluido': True, 'success': 'Ordem de troca criada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_caixa'))

def estorno_caixa(request):

    if request.method == 'POST':
            
        try:

            realizar_estorno_de_caixa(request)

            return JsonResponse({'concluido': True, 'success': 'Estorno realizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_caixa'))

def relatorio_caixa(request):

    if request.method == 'POST':
            
        try:

            error = gerar_relatorio_caixa(request)

            if error == '':

                return JsonResponse({'concluido': True, 'pdf_path': os.path.join(settings.MEDIA_URL, 'pdf/relatorio_caixa.pdf')})
            
            else:

                return JsonResponse({'concluido': False, 'erros': {'__all__': [error]}})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_caixa'))

@method_decorator(permission_required('financeiro.view_pdv'), name = 'dispatch')  
class SCInsertPDV(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_insert_pdv/sc_insert_pdv.html'
    model = STBOPROD

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        vendas = STBOPROD.objects.filter(fk_user = self.request.user)
        total = sum(venda.dvlrtotal for venda in vendas)
        context['total'] = total
        try:
            context['caixa'] = TBIOCX.objects.latest('pk')
        except:
            pass
        context['contas'] = CTBBANK.objects.all()
        context['tipopg'] = CTBITIPOPG.objects.all()
        context['juros'] = CTBJURO.objects.all()
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(fk_user = self.request.user)

def new_venda(request):

    if request.method == 'POST':
            
        try:

            vendas = definir_tabela(request)
            estoque = validar_estoque(request, vendas)
            adicionar_produto_a_lista(request, estoque, vendas)

            return JsonResponse({'concluido': True, 'success': 'Produto adicionado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

        except TBPROD.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Produto não encontrado!']}})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))
    
def delete_venda(request):

    if request.method == 'POST':
            
        try:

            vendas = definir_tabela(request)
            remover_produto_da_lista(request, vendas)

            return JsonResponse({'concluido': True, 'success': 'Produto removido da lista!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))

def delete_consignado(request):

    if request.method == 'POST':
            
        try:

            vendas = definir_tabela(request)
            remover_consignado_da_lista(request, vendas)

            return JsonResponse({'concluido': True, 'success': 'Produto removido da lista!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))

def qtd_consignado(request):

    if request.method == 'POST':
            
        try:

            vendas = definir_tabela(request)
            alterar_quantidade_consignado(request, vendas)

            return JsonResponse({'concluido': True, 'success': 'Quantidade alterada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))
    
def clear_venda(request):

    if request.method == 'POST':
            
        try:

            vendas = definir_tabela(request)
            remover_todos_os_produtos_da_lista(request, vendas)

            return JsonResponse({'concluido': True, 'success': 'Produtos removidos da lista!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))
    
def close_caixa(request):

    if request.method == 'POST':
            
        try:

            fechar_caixa()
            vendas = definir_tabela(request)
            remover_todos_os_produtos_da_lista(request, vendas)

            return JsonResponse({'concluido': True, 'success': 'Caixa fechado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))
    
def open_caixa(request):

    if request.method == 'POST':
            
        try:

            abrir_caixa()

            return JsonResponse({'concluido': True, 'success': 'Caixa aberto!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))

def new_sangria(request):

    if request.method == 'POST':
            
        try:

            realizar_sangria(request)

            return JsonResponse({'concluido': True, 'success': 'Sangria realizada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))
    
def new_desconto(request):

    if request.method == 'POST':
            
        try:

            vendas = definir_tabela(request)
            aplicar_desconto(request, vendas)

            return JsonResponse({'concluido': True, 'success': 'Desconto aplicado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))
    
def new_quantidade(request):

    if request.method == 'POST':
            
        try:

            vendas = definir_tabela(request)
            aplicar_quantidade(request, vendas)

            return JsonResponse({'concluido': True, 'success': 'Quantidade alterada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))
    
def pgdinheiro_venda(request):

    if request.method == 'POST':
            
        try:

            vendas = definir_tabela(request)
            caixa, desconto = nova_movimentacao_de_caixa(request)
            nova_saida_de_produtos(caixa, desconto, vendas)
            novo_pagamento(desconto, caixa)
            ajustar_estoque(request, vendas)
            ajustar_caixa(request)
            #uri = gerar_nf_venda(request, caixa, desconto, tipopg = 'DINHEIRO')

            if request.POST.get('id_venda_consignado'):
                fechar_consignado(request, vendas)
                remover_todos_os_produtos_da_lista(request, vendas)
                redirect_url = reverse('sc_list_consignado') + '?success=Venda+concluída!'
                return JsonResponse({'concluido': True, 'redirect_url': redirect_url})
            
            if request.POST.get('id_venda_troca'):
                fechar_troca(request, caixa, vendas)
                remover_todos_os_produtos_da_lista(request, vendas)
                redirect_url = reverse('sc_list_troca') + '?success=Venda+concluída!'
                return JsonResponse({'concluido': True, 'redirect_url': redirect_url})

            remover_todos_os_produtos_da_lista(request, vendas)

            return JsonResponse({'concluido': True, 'success': 'Venda concluída!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})
        
        except TBCLI.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Cliente não encontrado!']}})
        
        except User.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Vendedor não encontrado!']}})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))
    
def pgcartao_venda(request):

    if request.method == 'POST':
            
        try:

            vendas = definir_tabela(request)
            caixa, desconto = nova_movimentacao_de_caixa(request, tipopg = CTBITIPOPG.objects.get(pk = request.POST.get('dado_tipopg')))
            nova_saida_de_produtos(caixa, desconto, vendas)
            entrada_fin = novo_lancamento_financeiro(caixa)
            novo_pagamento(desconto, caixa, entrada_fin)
            ajustar_estoque(request, vendas)
            #uri = gerar_nf_venda(request, caixa, desconto, tipopg = 'CARTAO/PIX')

            if request.POST.get('id_venda_consignado'):
                fechar_consignado(request, vendas)
                remover_todos_os_produtos_da_lista(request, vendas)
                redirect_url = reverse('sc_list_consignado') + '?success=Venda+concluída!'
                return JsonResponse({'concluido': True, 'redirect_url': redirect_url})
            
            if request.POST.get('id_venda_troca'):
                fechar_troca(request, caixa, vendas)
                remover_todos_os_produtos_da_lista(request, vendas)
                redirect_url = reverse('sc_list_troca') + '?success=Venda+concluída!'
                return JsonResponse({'concluido': True, 'redirect_url': redirect_url})
            
            remover_todos_os_produtos_da_lista(request, vendas)

            return JsonResponse({'concluido': True, 'success': 'Venda concluída!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})
        
        except TBCLI.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Cliente não encontrado!']}})
        
        except User.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Vendedor não encontrado!']}})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))
    
def pgcrediario_venda(request):

    if request.method == 'POST':
            
        try:

            vendas = definir_tabela(request)
            caixa, desconto = nova_movimentacao_de_caixa_cred(request, qtdparc = int(request.POST.get('dado_parcela')))
            nova_saida_de_produtos(caixa, desconto, vendas)
            novo_lancamento_financeiro_crediario(request, caixa)
            ajustar_estoque(request, vendas)
            #uri = gerar_nf_venda(request, caixa, desconto, tipopg = 'CREDIARIO')

            if request.POST.get('id_venda_consignado'):
                fechar_consignado(request, vendas)
                remover_todos_os_produtos_da_lista(request, vendas)
                redirect_url = reverse('sc_list_consignado') + '?success=Venda+concluída!'
                return JsonResponse({'concluido': True, 'redirect_url': redirect_url})
            
            if request.POST.get('id_venda_troca'):
                fechar_troca(request, caixa, vendas)
                remover_todos_os_produtos_da_lista(request, vendas)
                redirect_url = reverse('sc_list_troca') + '?success=Venda+concluída!'
                return JsonResponse({'concluido': True, 'redirect_url': redirect_url})
            
            remover_todos_os_produtos_da_lista(request, vendas)

            return JsonResponse({'concluido': True, 'success': 'Venda concluída!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})
        
        except TBCLI.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Cliente não encontrado!']}})
        
        except User.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Vendedor não encontrado!']}})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))
    
def pgconsignado_venda(request):

    if request.method == 'POST':
            
        try:

            vendas = definir_tabela(request)
            consignado = novo_consignado(request, vendas)
            inserir_produtos_em_consignado(consignado, vendas)
            ajustar_estoque_consignado(vendas)
            remover_todos_os_produtos_da_lista(request, vendas)
            #uri = gerar_nf_consignado(request, consignado, tipopg = 'CONSIGNADO')

            return JsonResponse({'concluido': True, 'success': 'Consignado realizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})
        
        except TBCLI.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Cliente não encontrado!']}})
        
        except User.DoesNotExist:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Vendedor não encontrado!']}})

    else:
        return redirect(reverse_lazy('sc_insert_pdv'))

@method_decorator(permission_required('financeiro.view_transf'), name = 'dispatch')
class SCListTransf(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_transf/sc_list_transf.html'
    model = TBIOTRANSF
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['contas'] = CTBBANK.objects.all()
        if any([
            self.request.GET.get('search_dtinicio'),
            self.request.GET.get('search_dtfim')
        ]):
            context['filtrado'] = True
        return context

    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset()

        search_dtinicio = self.request.GET.get('search_dtinicio', '')
        search_dtfim = self.request.GET.get('search_dtfim', '')
        ordering = self.request.GET.get('ordering')

        if search_dtinicio:
            queryset = queryset.filter(dt__gte = search_dtinicio)
        if search_dtfim:
            dtfim_datetime = datetime.strptime(search_dtfim, '%Y-%m-%d')
            dtfim_endofday = dtfim_datetime + timedelta(days = 1) - timedelta(microseconds = 1)
            queryset = queryset.filter(dt__lte = dtfim_endofday)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

def new_transf(request):

    if request.method == 'POST':
            
        try:

            nova_transferencia(request)

            return JsonResponse({'concluido': True, 'success': 'Transferência realizada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_transf'))