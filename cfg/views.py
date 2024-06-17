from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import *
from django.http import JsonResponse
from .methods import *
from django.shortcuts import redirect
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .lists import Lists
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

@method_decorator(permission_required('cfg.view_usuarios'), name = 'dispatch')
class SCListUser(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_user/sc_list_user.html'
    model = User

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['profiles'] = CTBPROFILE.objects.all()
        return context

def new_password(request):

    if request.method == 'POST':
            
        try:

            editar_senha_usuario(request)

            return JsonResponse({'concluido': True, 'success': 'Senha redefinida!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_user'))

def new_user(request):

    if request.method == 'POST':
            
        try:

            user = criar_novo_usuario(request)
            criar_profile_para_usuario(user)

            return JsonResponse({'concluido': True, 'success': 'Usuário cadastrado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

        except IntegrityError:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Usuário já cadastrado!']}})

    else:
        return redirect(reverse_lazy('sc_list_user'))
    
def edit_user(request):

    if request.method == 'POST':
            
        try:

            editar_usuario_existente(request)

            return JsonResponse({'concluido': True, 'success': 'Usuário atualizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

        except IntegrityError:

            return JsonResponse({'concluido': False, 'erros': {'__all__': ['Usuário já cadastrado!']}})

    else:
        return redirect(reverse_lazy('sc_list_user'))
    
def acessos_user(request):

    if request.method == 'POST':
            
        try:
            definir_acessos(request)

            return JsonResponse({'concluido': True, 'success': 'Usuário atualizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_user'))


@method_decorator(permission_required('cfg.view_categorias'), name = 'dispatch')   
class SCListCategoria(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_categoria/sc_list_categoria.html'
    model = CTBCATPROD
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        if self.request.GET.get('search_desc'):
            context['filtrado'] = True
        return context

    def get_queryset(self) -> QuerySet[Any]:
        
        queryset = super().get_queryset()

        search_desc = self.request.GET.get('search_desc', '')
        ordering = self.request.GET.get('ordering')

        if search_desc:
            queryset = queryset.filter(dsc__icontains = search_desc)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
    
def new_categoria(request):

    if request.method == 'POST':
            
        try:

            criar_nova_categoria(request)

            return JsonResponse({'concluido': True, 'success': 'Categoria cadastrada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_categoria'))
    
def edit_categoria(request):

    if request.method == 'POST':
            
        try:

            editar_categoria_existente(request)

            return JsonResponse({'concluido': True, 'success': 'Categoria atualizada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_categoria'))

@method_decorator(permission_required('cfg.view_custos'), name = 'dispatch')  
class SCListCusto(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_custo/sc_list_custo.html'
    model = CTBCATFIN
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        if self.request.GET.get('search_desc'):
            context['filtrado'] = True
        return context

    def get_queryset(self) -> QuerySet[Any]:
        
        queryset = super().get_queryset()

        search_desc = self.request.GET.get('search_desc', '')
        ordering = self.request.GET.get('ordering')

        if search_desc:
            queryset = queryset.filter(dsc__icontains = search_desc)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
    
def new_custo(request):

    if request.method == 'POST':
            
        try:

            criar_novo_custo(request)

            return JsonResponse({'concluido': True, 'success': 'Tipo de custo cadastrado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_custo'))
    
def edit_custo(request):

    if request.method == 'POST':
            
        try:

            editar_custo_existente(request)

            return JsonResponse({'concluido': True, 'success': 'Tipo de custo atualizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_custo'))

@method_decorator(permission_required('cfg.view_juros'), name = 'dispatch')   
class SCListJuro(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_juro/sc_list_juro.html'
    model = CTBJURO
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['juro'] = CTBJURO.objects.all()
        return context

    def get_queryset(self) -> QuerySet[Any]:
        
        queryset = super().get_queryset()

        search_porc = self.request.GET.get('search_porc', '')
        ordering = self.request.GET.get('ordering')

        if search_porc:
            queryset = queryset.filter(pvlr = search_porc)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
    
def new_juro(request):

    if request.method == 'POST':
            
        try:

            criar_novo_juro(request)

            return JsonResponse({'concluido': True, 'success': 'Porcentagem de juro cadastrada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_juro'))
    
def edit_juro(request):

    if request.method == 'POST':
            
        try:

            editar_juro_existente(request)

            return JsonResponse({'concluido': True, 'success': 'Porcentagem de juro atualizada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_juro'))

@method_decorator(permission_required('cfg.view_contas'), name = 'dispatch')    
class SCListConta(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_conta/sc_list_conta.html'
    model = CTBBANK
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['bancos'] = Lists.list_bancos
        if any([
            self.request.GET.get('search_razao'),
            self.request.GET.get('search_banco'),
            self.request.GET.get('search_ag'),
            self.request.GET.get('search_conta'),
            self.request.GET.get('search_pix')
        ]):
            context['filtrado'] = True
        return context

    def get_queryset(self) -> QuerySet[Any]:
        
        queryset = super().get_queryset()

        search_razao = self.request.GET.get('search_razao', '')
        search_banco = self.request.GET.get('search_banco', '')
        search_ag = self.request.GET.get('search_ag', '')
        search_conta = self.request.GET.get('search_conta', '')
        search_pix = self.request.GET.get('search_pix', '')
        ordering = self.request.GET.get('ordering')

        if search_razao:
            queryset = queryset.filter(razao__icontains = search_razao)
        if search_banco:
            matching_codes = [code for code, name in Lists.list_bancos if search_banco.lower() in name.lower()]
            if matching_codes:
                queryset = queryset.filter(banco__in = matching_codes)
        if search_ag:
            queryset = queryset.filter(ag__icontains = search_ag)
        if search_conta:
            queryset = queryset.filter(conta__icontains = search_conta)
        if search_pix:
            queryset = queryset.filter(pix__icontains = search_pix)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
    
def new_conta(request):

    if request.method == 'POST':
            
        try:

            criar_nova_conta(request)

            return JsonResponse({'concluido': True, 'success': 'Conta bancária cadastrada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_conta'))
    
def edit_conta(request):

    if request.method == 'POST':
            
        try:

            editar_conta_existente(request)

            return JsonResponse({'concluido': True, 'success': 'Conta bancária atualizada!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_conta'))

@method_decorator(permission_required('cfg.view_pagamentos'), name = 'dispatch')   
class SCListTipoPG(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('sc_login')
    template_name = 'sc_list_tipopg/sc_list_tipopg.html'
    model = CTBITIPOPG
    paginate_by = 25
    ordering = ['-id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['contas'] = CTBBANK.objects.all()
        if self.request.GET.get('search_desc'):
            context['filtrado'] = True
        return context

    def get_queryset(self) -> QuerySet[Any]:
        
        queryset = super().get_queryset()

        search_desc = self.request.GET.get('search_desc', '')
        ordering = self.request.GET.get('ordering')

        if search_desc:
            queryset = queryset.filter(dsc__icontains = search_desc)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
    
def new_tipopg(request):

    if request.method == 'POST':
            
        try:

            criar_novo_tipopg(request)

            return JsonResponse({'concluido': True, 'success': 'Tipo de pagamento cadastrado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_tipopg'))
    
def edit_tipopg(request):

    if request.method == 'POST':
            
        try:

            editar_tipopg_existente(request)

            return JsonResponse({'concluido': True, 'success': 'Tipo de pagamento atualizado!'})
        
        except ValidationError as e:

            return JsonResponse({'concluido': False, 'erros': e.message_dict})

    else:
        return redirect(reverse_lazy('sc_list_tipopg'))