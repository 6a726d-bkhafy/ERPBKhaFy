from django.urls import path
from .views import *

urlpatterns = [
    path('', SCListCompra.as_view(), name = 'sc_list_compra'),
    path('entrada-compra', entrada_compra, name = 'entrada_compra'),
    path('nova-ordem/<int:fk>', SCInsertCompra.as_view(), name = 'sc_insert_compra'),
    path('nova-ordem/add-item-compra/<int:fk>', add_item_compra, name = 'add_item_compra'),
    path('nova-ordem/delete-compra', delete_compra, name = 'delete_compra'),
    path('nova-ordem/clear-compra/<int:fk>', clear_compra, name = 'clear_compra'),
    path('nova-ordem/qtd-compra', qtd_compra, name = 'qtd_compra'),
    path('nova-ordem/confirm-compra/<int:fk>', confirm_compra, name = 'confirm_compra'),
    path('estorno', estorno_compra, name = 'estorno_compra'),

    path('lotes', SCListLote.as_view(), name = 'sc_list_lote'),
    path('entrada-lote', entrada_lote, name = 'entrada_lote'),
    path('novo-lote/<int:fk>', SCInsertLote.as_view(), name = 'sc_insert_lote'),
    path('novo-lote/add-item-lote/<int:fk>', add_item_lote, name = 'add_item_lote'),
    path('novo-lote/delete-lote', delete_lote, name = 'delete_lote'),
    path('novo-lote/clear-lote/<int:fk>', clear_lote, name = 'clear_lote'),
    path('novo-lote/qtd-lote', qtd_lote, name = 'qtd_lote'),
    path('novo-lote/confirm-lote/<int:fk>', confirm_lote, name = 'confirm_lote'),
    path('estornolt', estorno_lote, name = 'estorno_lote'),
    path('new-etiquetas', new_etiquetas, name = 'new_etiquetas'),
    path('relatorio', relatorio_compra, name = 'relatorio_compra'),
]