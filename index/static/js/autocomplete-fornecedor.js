$(function() {
    $("#dado_fornecedor_desc").autocomplete({
        source: "/inicio/autocomplete/fornecedor-by-desc",
        minLength: 2,
        messages: {
            noResults: '',
            results: function() {}
        },
        select: function(event, ui) {
            $("#id_fornecedor").val(ui.item.pk);
        }
    });

    $("#id_fornecedor").on("change", function() {
        fetchDataAndUpdateFields($(this).val());
    });

    function fetchDataAndUpdateFields(pk) {
        let url = `/inicio/autocomplete/fornecedor-by-pk/${pk}`;

        $.getJSON(url, function(data) {
            $("#dado_fornecedor_desc").val(data.desc);
        });
    }
});
