from django.urls import path
from .views import *

urlpatterns = [
    path('', SCViewIndex.as_view(), name = 'sc_index'),
    path('perfil', new_profile, name = 'new_profile'),
    path('search', search, name = 'search'),
]

urlpatterns += [
    path('autocomplete/produto-by-pk/<int:pk>', produto_by_pk, name = 'produto_by_pk'),
    path('autocomplete/produto-by-desc', produto_by_desc, name = 'produto_by_desc'),
]

urlpatterns += [
    path('autocomplete/fornecedor-by-pk/<int:pk>', fornecedor_by_pk, name = 'fornecedor_by_pk'),
    path('autocomplete/fornecedor-by-desc', fornecedor_by_desc, name = 'fornecedor_by_desc'),
]

urlpatterns += [
    path('autocomplete/cliente-by-pk/<int:pk>', cliente_by_pk, name = 'cliente_by_pk'),
    path('autocomplete/cliente-by-desc', cliente_by_desc, name = 'cliente_by_desc'),
]

urlpatterns += [
    path('autocomplete/usuario-by-pk/<int:pk>', usuario_by_pk, name = 'usuario_by_pk'),
    path('autocomplete/usuario-by-desc', usuario_by_desc, name = 'usuario_by_desc'),
]

urlpatterns += [
    path('grafico/vendas/<int:parameter>', grafico_vendas, name = 'grafico_vendas'),
    path('grafico/categorias/<int:parameter>', grafico_categorias, name = 'grafico_categorias'),
    path('grafico/custos/<int:parameter>', grafico_custos, name = 'grafico_custos'),
]

urlpatterns += [
    path('relatorio', Relatorio.as_view(), name = 'relatorio'),
]