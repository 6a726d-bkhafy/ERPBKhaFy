$(document).ready(function() {
    $.get('/inicio/search', function(data) {
        var linkSuggestions = [
            { name: "Usuários", url: data.sc_list_user },
            { name: "Categorias de Produto", url: data.sc_list_categoria },
            { name: "Tipos de Custo", url: data.sc_list_custo },
            { name: "Tabela de Juros", url: data.sc_list_juro },
            { name: "Contas Bancárias", url: data.sc_list_conta },
            { name: "Clientes", url: data.sc_list_cliente },
            { name: "Fornecedores", url: data.sc_list_fornecedor },
            { name: "Produtos", url: data.sc_list_produto },
            { name: "Etiquetas", url: data.sc_insert_etiqueta },
            { name: "Inventários", url: data.sc_list_inventario },
            { name: "Ordem de Compra", url: data.sc_list_compra },
            { name: "PDV", url: data.sc_insert_pdv },
            { name: "Contas a Pagar", url: data.sc_list_saida_financeiro },
            { name: "Contas a Receber", url: data.sc_list_entrada_financeiro },
            { name: "Movimentação de Caixa", url: data.sc_list_caixa },
            { name: "Consignados", url: data.sc_list_consignado },
            { name: "Troca de Produto", url: data.sc_list_troca },
            { name: "Tipos de Pagamento", url: data.sc_list_tipopg },
            { name: "Transferência Entre Contas", url: data.sc_list_transf },
        ];

        linkSuggestions = linkSuggestions.filter(item => item.url);
        
        $("#search-input").autocomplete({
            source: linkSuggestions.map(item => item.name),
            minLength: 2,
            messages: false,
            select: function(event, ui) {
                window.location.href = linkSuggestions.find(item => item.name === ui.item.value).url;
            }
        });
    });
});
