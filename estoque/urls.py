from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('produtos/', SCListProduto.as_view(), name = 'sc_list_produto'),
    path('produtos/new-produto', new_produto, name = 'new_produto'),
    path('produtos/edit-produto', edit_produto, name = 'edit_produto'),
    path('produtos/edit-preco', edit_preco, name = 'edit_preco'),
    path('produtos/altera_custo', altera_custo, name = 'change_custo'),
    path('produtos/relatorio/estoque', relatorio_estoque, name = 'relatorio_estoque'),
    path('produtos/relatorio/consignado', relatorio_consignado, name = 'relatorio_consignado'),
]

urlpatterns += [
    path('etiquetas', SCInsertEtiqueta.as_view(), name = 'sc_insert_etiqueta'),
    path('etiquetas/new-etiqueta', new_etiqueta, name = 'new_etiqueta'),
    path('etiquetas/delete-etiqueta', delete_etiqueta, name = 'delete_etiqueta'),
    path('etiquetas/clear-etiqueta', clear_etiqueta, name = 'clear_etiqueta'),
    path('etiquetas/confirm-etiqueta', confirm_etiqueta, name = 'confirm_etiqueta'),
]

urlpatterns += [
    path('inventarios', SCListInventario.as_view(), name = 'sc_list_inventario'),
    path('inventarios/novo-inventario', SCInsertInventario.as_view(), name = 'sc_insert_inventario'),
    path('inventarios/novo-inventario/new-inventario', new_inventario, name = 'new_inventario'),
    path('inventarios/novo-inventario/delete-inventario', delete_inventario, name = 'delete_inventario'),
    path('inventarios/novo-inventario/clear-inventario', clear_inventario, name = 'clear_inventario'),
    path('inventarios/novo-inventario/confirm-inventario', confirm_inventario, name = 'confirm_inventario'),
]

urlpatterns += [
    path('consignados', SCListConsignado.as_view(), name = 'sc_list_consignado'),
    path('consignados/devolucao_consignado', devolucao_consignado, name = 'devolucao_consignado'),
    path('consignados/pdv/<int:fk>', SCInsertConsignado.as_view(), name = 'sc_insert_consignado'),
]

urlpatterns += [
    path('trocas', SCListTroca.as_view(), name = 'sc_list_troca'),
    path('trocas/pdv/<int:fk>', SCInsertTroca.as_view(), name = 'sc_insert_troca'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)