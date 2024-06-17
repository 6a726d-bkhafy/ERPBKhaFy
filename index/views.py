from typing import Any
from .methods import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from financeiro.models import TBOPROD
from compras.models import TBIPROD

class SCViewIndex(LoginRequiredMixin, TemplateView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)

        produtos = TBOPROD.objects.filter(Q(sts = '0') | Q(sts = '5')).order_by('-pk')[:10]
        caixa = [prod.fk_tbcx for prod in produtos]

        compras = TBIPROD.objects.filter(~Q(sts = '2')).order_by('-pk')[:10]

        if self.request.GET.get('fcard') == '2':
            total_vendas = TBCX.objects.filter(dt__month = datetime.now().month).count()
        elif self.request.GET.get('fcard') == '3':
            total_vendas = TBCX.objects.filter(dt__year = datetime.now().year).count()
        else:
            total_vendas = TBCX.objects.filter(dt__icontains = datetime.now().date()).count()

        if self.request.GET.get('scard') == '2':
            faturamento = sum(i.dvlr for i in TBIPG.objects.filter(dtpg__month = datetime.now().month))
        elif self.request.GET.get('scard') == '3':
            faturamento = sum(i.dvlr for i in TBIPG.objects.filter(dtpg__year = datetime.now().year))
        else:
            faturamento = sum(i.dvlr for i in TBIPG.objects.filter(dtpg__icontains = datetime.now().date()))

        context['produtos'] = produtos
        context['caixa'] = list(set(caixa))
        context['total_vendas'] = total_vendas
        context['faturamento'] = faturamento
        context['compras'] = compras

        return context

def new_profile(request):

    if request.method == 'POST':
            
        try:

            atualizar_imagem_do_perfil(request)

            return JsonResponse({'concluido': True, 'success': 'Imagem de perfil atualizada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_user'))

def search(request):

    return buscar_por_tela(request)

def produto_by_pk(request, pk):

    return buscar_produto_por_pk(pk)

def produto_by_desc(request):

    return buscar_produto_por_desc(request)

def fornecedor_by_pk(request, pk):

    return buscar_fornecedor_por_pk(pk)

def fornecedor_by_desc(request):

    return buscar_fornecedor_por_desc(request)

def cliente_by_pk(request, pk):

    return buscar_cliente_por_pk(pk)

def cliente_by_desc(request):

    return buscar_cliente_por_desc(request)

def usuario_by_pk(request, pk):

    return buscar_usuario_por_pk(pk)

def usuario_by_desc(request):

    return buscar_usuario_por_desc(request)

def grafico_vendas(request, parameter):

    return grafico_vendas_data(parameter)

def grafico_categorias(request, parameter):

    return grafico_categorias_data(parameter)

def grafico_custos(request, parameter):

    return grafico_custos_data(parameter)

class Relatorio(TemplateView):

    template_name = 'relatorios/relatorio.html'