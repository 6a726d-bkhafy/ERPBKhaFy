$(function() {
    $("#dado_produto_desc").autocomplete({
        source: "/inicio/autocomplete/produto-by-desc",
        minLength: 2,
        messages: {
            noResults: '',
            results: function() {}
        },
        select: function(event, ui) {
            $("#id_produto").val(ui.item.pk);
        }
    });

    $("#id_produto").on("change", function() {
        fetchDataAndUpdateFields($(this).val());
    });

    function fetchDataAndUpdateFields(pk) {
        let url = `/inicio/autocomplete/produto-by-pk/${pk}`;

        $.getJSON(url, function(data) {
            $("#dado_produto_desc").val(data.desc);
        });
    }
});
