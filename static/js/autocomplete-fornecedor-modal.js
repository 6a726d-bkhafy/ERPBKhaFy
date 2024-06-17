$(document).ready(function() {

    $('#modal-new-convencional').on('shown.bs.modal', function() {
        initializeAutocomplete();
    });

    $('#modal-filter-list-saida-financeiro').on('shown.bs.modal', function() {
        initializeAutocompleteFilter();
    });

    $('#modal-filter-list-compra').on('shown.bs.modal', function() {
        initializeAutocomplete();
    });

    $('#modal-relatorio').on('shown.bs.modal', function() {
        initializeAutocompleteRel();
    });

    function initializeAutocomplete() {
        $("#dado_fornecedor_desc").autocomplete({
            source: "/inicio/autocomplete/fornecedor-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_fornecedor").val(ui.item.pk);
            },
            messages: {
                noResults: '',
                results: function() {}
            },
            open: function() {
                $('.ui-autocomplete').css('z-index', 10000);
            }
        });
    }

    $("#id_fornecedor").on("change", function() {
        fetchDataAndUpdateFields($(this).val());
    });

    function fetchDataAndUpdateFields(pk) {
        let url = `/inicio/autocomplete/fornecedor-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_fornecedor_desc").val(data.desc);
        });
    }

    function initializeAutocompleteFilter() {
        $("#dado_fornecedor_desc_filter").autocomplete({
            source: "/inicio/autocomplete/fornecedor-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_fornecedor_filter").val(ui.item.pk);
            },
            messages: {
                noResults: '',
                results: function() {}
            },
            open: function() {
                $('.ui-autocomplete').css('z-index', 10000);
            }
        });
    }

    $("#id_fornecedor_filter").on("change", function() {
        fetchDataAndUpdateFieldsFilter($(this).val());
    });

    function fetchDataAndUpdateFieldsFilter(pk) {
        let url = `/inicio/autocomplete/fornecedor-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_fornecedor_desc_filter").val(data.desc);
        });
    }

    function initializeAutocompleteRel() {
        $("#dado_fornecedor_desc_rel").autocomplete({
            source: "/inicio/autocomplete/fornecedor-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_fornecedor_rel").val(ui.item.pk);
            },
            messages: {
                noResults: '',
                results: function() {}
            },
            open: function() {
                $('.ui-autocomplete').css('z-index', 10000);
            }
        });
    }

    $("#id_fornecedor_rel").on("change", function() {
        fetchDataAndUpdateFieldsRel($(this).val());
    });

    function fetchDataAndUpdateFieldsRel(pk) {
        let url = `/inicio/autocomplete/fornecedor-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_fornecedor_desc_rel").val(data.desc);
        });
    }

});

