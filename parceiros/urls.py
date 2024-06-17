from django.urls import path
from .views import *

urlpatterns = [
    path('clientes', SCListCliente.as_view(), name = 'sc_list_cliente'),
    path('clientes/new-cliente', new_cliente, name = 'new_cliente'),
    path('clientes/edit-cliente', edit_cliente, name = 'edit_cliente'),
    path('clientes/new-limite', new_limite, name = 'new_limite'),
    path('clientes/lock-cliente', lock_cliente, name = 'lock_cliente'),
    path('clientes/unlock-cliente', unlock_cliente, name = 'unlock_cliente'),
]   

urlpatterns += [
    path('fornecedores', SCListFornecedor.as_view(), name = 'sc_list_fornecedor'),
    path('fornecedores/new-forn', new_forn, name = 'new_forn'),
    path('fornecedores/edit-forn', edit_forn, name = 'edit_forn'),
]

urlpatterns += [
    path('agenda-cliente', SCListAgendaCliente.as_view(), name = 'sc_agenda_cliente'),
    path('agenda-cliente/new-agenda-cliente', new_agenda_cliente, name = 'new_agenda_cliente'),
    path('agenda-cliente/edit-agenda-cliente', edit_agenda_cliente, name = 'edit_agenda_cliente'),
]

urlpatterns += [
    path('agenda-forn', SCListAgendaFornecedor.as_view(), name = 'sc_agenda_forn'),
    path('forn/new-agenda-forn', new_agenda_forn, name = 'new_agenda_forn'),
    path('forn/edit-agenda-forn', edit_agenda_forn, name = 'edit_agenda_forn'),
]