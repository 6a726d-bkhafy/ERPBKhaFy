from django.urls import path
from .views import *

urlpatterns = [
    path('saida', SCListSaidaFinanceiro.as_view(), name = 'sc_list_saida_financeiro'),
    path('saida/new-lancamento', new_lancamento, name = 'new_lancamento'),
    path('saida/new-pagamento', new_pagamento, name = 'new_pagamento'),
    path('saida/estorno-pagamento', estorno_pagamento_saida, name = 'estorno_pagamento_saida'),
    path('saida/new-venc', new_venc_saida, name = 'new_venc_saida'),
    path('saida/estorno-lanc', estorno_lanc, name = 'estorno_lanc'),
    path('saida/edit-parcelas', edit_parcelas_saida, name = 'edit_parcelas_saida'),
    path('saida/relatorio', relatorio_saida, name = 'relatorio_saida'),
]

urlpatterns += [
    path('entrada', SCListEntradaFinanceiro.as_view(), name = 'sc_list_entrada_financeiro'),
    path('entrada/new-pagamento-dinheiro', new_pagamento_entrada_dinheiro, name = 'new_pagamento_entrada_dinheiro'),
    path('entrada/new-pagamento-outros', new_pagamento_entrada_outros, name = 'new_pagamento_entrada_outros'),
    path('entrada/estorno-pagamento', estorno_pagamento_entrada, name = 'estorno_pagamento_entrada'),
    path('entrada/new-venc', new_venc_entrada, name = 'new_venc_entrada'),
    path('entrada/edit-parcelas', edit_parcelas, name = 'edit_parcelas'),
    path('entrada/relatorio', relatorio_entrada, name = 'relatorio_entrada'),
]

urlpatterns += [
    path('caixa', SCListCaixa.as_view(), name = 'sc_list_caixa'),
    path('caixa/new-troca', new_troca, name = 'new_troca'),
    path('caixa/estorno', estorno_caixa, name = 'estorno_caixa'),
    path('caixa/relatorio', relatorio_caixa, name = 'relatorio_caixa'),
]

urlpatterns += [
    path('pdv', SCInsertPDV.as_view(), name = 'sc_insert_pdv'),
    path('pdv/new-venda', new_venda, name = 'new_venda'),
    path('pdv/delete-venda', delete_venda, name = 'delete_venda'),
    path('pdv/delete-consignado', delete_consignado, name = 'delete_consignado'),
    path('pdv/qtd-consignado', qtd_consignado, name = 'qtd_consignado'),
    path('pdv/clear-venda', clear_venda, name = 'clear_venda'),
    path('pdv/close-caixa', close_caixa, name = 'close_caixa'),
    path('pdv/open-caixa', open_caixa, name = 'open_caixa'),
    path('pdv/new-sangria', new_sangria, name = 'new_sangria'),
    path('pdv/new-desconto', new_desconto, name = 'new_desconto'),
    path('pdv/new-quantidade', new_quantidade, name = 'new_quantidade'),
    path('pdv/pgdinheiro-venda', pgdinheiro_venda, name = 'pgdinheiro_venda'),
    path('pdv/pgcartao-venda', pgcartao_venda, name = 'pgcartao_venda'),
    path('pdv/pgcrediario-venda', pgcrediario_venda, name = 'pgcrediario_venda'),
    path('pdv/pgconsignado-venda', pgconsignado_venda, name = 'pgconsignado_venda'),
]

urlpatterns += [
    path('transferencia', SCListTransf.as_view(), name = 'sc_list_transf'),
    path('transferencia/new-transf', new_transf, name = 'new_transf'),
]
