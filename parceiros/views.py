from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import *
from django.http import JsonResponse
from django.shortcuts import redirect
from .methods import *
from .lists import Lists
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from django.db.models import Q


@method_decorator(permission_required('parceiros.view_clientes'), name = 'dispatch')
class SCListCliente(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_cliente/sc_list_cliente.html'
    model = TBCLI
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['estados'] = Lists.list_estados
        context['tipos'] = Lists.list_tipo_cli
        if any([
            self.request.GET.get('search_id'), 
            self.request.GET.get('search_desc'),
            self.request.GET.get('search_doc')
        ]):
            context['filtrado'] = True
        return context
    
    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset()

        search_id = self.request.GET.get('search_id', '')
        search_desc = self.request.GET.get('search_desc', '')
        search_doc = self.request.GET.get('search_doc', '')
        ordering = self.request.GET.get('ordering')

        if search_id:
            queryset = queryset.filter(id = search_id)
        if search_desc:
            queryset = queryset.filter(dsc__icontains = search_desc)
        if search_doc:
            queryset = queryset.filter(doc__icontains = search_doc)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
    
def new_cliente(request):

    if request.method == 'POST':
            
        try:

            criar_novo_cliente(request)

            return JsonResponse({'concluido': True, 'success': 'Cliente cadastrado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_cliente'))
    
def edit_cliente(request):

    if request.method == 'POST':
            
        try:

            editar_cliente_existente(request)

            return JsonResponse({'concluido': True, 'success': 'Cliente atualizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_cliente'))

def new_limite(request):

    if request.method == 'POST':
            
        try:

            alterar_limite(request)

            return JsonResponse({'concluido': True, 'success': 'Limite alterado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_cliente'))
    
def lock_cliente(request):

    if request.method == 'POST':
            
        try:

            travar_cliente(request)

            return JsonResponse({'concluido': True, 'success': 'Limite travado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_cliente'))

def unlock_cliente(request):

    if request.method == 'POST':
            
        try:

            destravar_cliente(request)

            return JsonResponse({'concluido': True, 'success': 'Limite destravado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_cliente'))

@method_decorator(permission_required('parceiros.view_fornecedores'), name = 'dispatch')
class SCListFornecedor(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_forn/sc_list_forn.html'
    model = TBFORN
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['estados'] = Lists.list_estados
        if any([
            self.request.GET.get('search_id'), 
            self.request.GET.get('search_desc'),
            self.request.GET.get('search_doc')
        ]):
            context['filtrado'] = True
        return context
    
    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset()

        search_id = self.request.GET.get('search_id', '')
        search_desc = self.request.GET.get('search_desc', '')
        search_doc = self.request.GET.get('search_doc', '')
        ordering = self.request.GET.get('ordering')

        if search_id:
            queryset = queryset.filter(id = search_id)
        if search_desc:
            queryset = queryset.filter(razao__icontains = search_desc)
        if search_doc:
            queryset = queryset.filter(doc__icontains = search_doc)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

def new_forn(request):

    if request.method == 'POST':
            
        try:

            criar_novo_fornecedor(request)

            return JsonResponse({'concluido': True, 'success': 'Fornecedor cadastrado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_forn'))
    
def edit_forn(request):

    if request.method == 'POST':
            
        try:

            editar_fornecedor_existente(request)

            return JsonResponse({'concluido': True, 'success': 'Fornecedor atualizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_forn'))


class SCListAgendaCliente(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_agenda_cliente/sc_agenda_cliente.html'
    model = TBAGENDACLI
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['sts'] = Lists.list_sts_agenda
        context['tipo'] = Lists.list_tipo_contato
        if self.request.GET.get('search_cli'):
            cli = TBCLI.objects.filter(pk=self.request.GET.get('search_cli')).first()
            context['cliente'] = cli if cli else None
        if self.request.GET.get('search_func'):
            func = User.objects.filter(pk=self.request.GET.get('search_func')).first()
            if func:
                context['funcionario'] = f'{func.first_name} {func.last_name}'
            else:
                context['funcionario'] = None
        if any([
            self.request.GET.get('search_id'), 
            self.request.GET.get('search_func'),
            self.request.GET.get('search_cli'),
            self.request.GET.get('search_dtinicio'),
            self.request.GET.get('search_dtfim'),
            self.request.GET.get('search_sts'),
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
        search_sts = self.request.GET.get('search_sts', '')
        ordering = self.request.GET.get('ordering')

        if search_id:
            queryset = queryset.filter(pk = search_id)
        if search_func:
            queryset = queryset.filter(fk_user__pk = search_func)
        if search_cli:
            queryset = queryset.filter(fk_tbcli__pk = search_cli)
        if search_dtinicio:
            queryset = queryset.filter(dthr__gte = search_dtinicio)
        if search_dtfim:
            dtfim_datetime = datetime.strptime(search_dtfim, '%Y-%m-%d')
            dtfim_endofday = dtfim_datetime + timedelta(days = 1) - timedelta(microseconds = 1)
            queryset = queryset.filter(dthr__lte = dtfim_endofday)
        if search_sts:
            queryset = queryset.filter(stsagendacli = search_sts)
        if ordering:
            queryset = queryset.order_by(ordering)


        return queryset
    
def new_agenda_cliente(request):

    if request.method == 'POST':
            
        try:

            criar_novo_agenda_cliente(request)

            return JsonResponse({'concluido': True, 'success': 'Contato cadastrado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_agenda_cliente'))
    
def edit_agenda_cliente(request):

    if request.method == 'POST':
            
        try:

            editar_agenda_cliente_existente(request)

            return JsonResponse({'concluido': True, 'success': 'Agenda atualizada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_agenda_cliente'))

class SCListAgendaFornecedor(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_agenda_forn/sc_agenda_forn.html'
    model = TBAGENDAFORN
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['sts'] = Lists.list_sts_agenda
        context['tipo'] = Lists.list_tipo_contato
        if self.request.GET.get('search_forn'):
            forn = TBFORN.objects.filter(pk=self.request.GET.get('search_forn')).first()
            context['fornecedor'] = forn if forn else None
        if self.request.GET.get('search_func'):
            func = User.objects.filter(pk=self.request.GET.get('search_func')).first()
            if func:
                context['funcionario'] = f'{func.first_name} {func.last_name}'
            else:
                context['funcionario'] = None
        if any([
            self.request.GET.get('search_id'), 
            self.request.GET.get('search_func'),
            self.request.GET.get('search_forn'),
            self.request.GET.get('search_dtinicio'),
            self.request.GET.get('search_dtfim'),
            self.request.GET.get('search_sts'),
        ]):
            context['filtrado'] = True
        return context
    
    def get_queryset(self) -> QuerySet[Any]:

        queryset = super().get_queryset()

        search_id = self.request.GET.get('search_id', '')
        search_func = self.request.GET.get('search_func', '')
        search_forn = self.request.GET.get('search_forn', '')
        search_dtinicio = self.request.GET.get('search_dtinicio', '')
        search_dtfim = self.request.GET.get('search_dtfim', '')
        search_sts = self.request.GET.get('search_sts', '')
        ordering = self.request.GET.get('ordering')

        if search_id:
            queryset = queryset.filter(pk = search_id)
        if search_func:
            queryset = queryset.filter(fk_user__pk = search_func)
        if search_forn:
            queryset = queryset.filter(fk_tbforn__pk = search_forn)

        if search_dtinicio:
            queryset = queryset.filter(dthr__gte = search_dtinicio)
        if search_dtfim:
            dtfim_datetime = datetime.strptime(search_dtfim, '%Y-%m-%d')
            dtfim_endofday = dtfim_datetime + timedelta(days = 1) - timedelta(microseconds = 1)
            queryset = queryset.filter(dthr__lte = dtfim_endofday)
        if search_sts:
            if search_sts == '0':
                queryset = queryset.filter(Q(stsagendaforn = '0') | Q(stsagendaforn = '4'))
            else:
                queryset = queryset.filter(stsagendaforn = search_sts)

        if ordering:
            queryset = queryset.order_by(ordering)


        return queryset

def new_agenda_forn(request):

    if request.method == 'POST':
            
        try:

            criar_novo_agenda_forn(request)

            return JsonResponse({'concluido': True, 'success': 'Contato cadastrado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_agenda_forn'))
    
def edit_agenda_forn(request):

    if request.method == 'POST':
            
        try:

            editar_agenda_forn_existente(request)

            return JsonResponse({'concluido': True, 'success': 'Agenda atualizada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_agenda_forn'))