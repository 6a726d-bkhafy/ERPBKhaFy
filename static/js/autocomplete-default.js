$(function() {
    $("#dado_campo").autocomplete({
        source: "insert/search-campo-default",
        minLength: 2,
        select: function(event, ui) {
            $("#id_tb_default").val(ui.item.pk);
        }
    });

    $("#id_tb_default").on("change", function() {
        fetchDataAndUpdateFields($(this).val());
    });

    function fetchDataAndUpdateFields(pk) {
        let url = `insert/search-pk-default/${pk}`;

        $.getJSON(url, function(data) {
            $("#dado_campo").val(data.campo);
        });
    }
});
