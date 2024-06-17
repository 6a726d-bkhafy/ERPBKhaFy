$(document).ready(function() {

    $('#modal-pgdinheiro-venda').on('shown.bs.modal', function() {
        initializeAutocomplete();
    });

    $('#modal-pgcartao-venda').on('shown.bs.modal', function() {
        initializeAutocompleteCartao();
    });

    $('#modal-pgcrediario-venda').on('shown.bs.modal', function() {
        initializeAutocompleteCred();
    });

    $('#modal-pgconsignado-venda').on('shown.bs.modal', function() {
        initializeAutocompleteCons();
    });

    $('#modal-filter-list-caixa').on('shown.bs.modal', function() {
        initializeAutocomplete();
    });

    $('#modal-filter-list-compra').on('shown.bs.modal', function() {
        initializeAutocomplete();
    });

    $('#modal-filter-list-consignado').on('shown.bs.modal', function() {
        initializeAutocomplete();
    });

    $('#modal-filter-list-inventario').on('shown.bs.modal', function() {
        initializeAutocomplete();
    });

    $('#modal-relatorio').on('shown.bs.modal', function() {
        initializeAutocompleteRel();
    });

    function initializeAutocomplete() {
        $("#dado_usuario_desc").autocomplete({
            source: "/inicio/autocomplete/usuario-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_usuario").val(ui.item.pk);
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

    $("#id_usuario").on("change", function() {
        fetchDataAndUpdateFields($(this).val());
    });

    function fetchDataAndUpdateFields(pk) {
        let url = `/inicio/autocomplete/usuario-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_usuario_desc").val(data.username);
        });
    }

    function initializeAutocompleteCartao() {
        $("#dado_usuario_desc_cartao").autocomplete({
            source: "/inicio/autocomplete/usuario-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_usuario_cartao").val(ui.item.pk);
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

    $("#id_usuario_cartao").on("change", function() {
        fetchDataAndUpdateFieldsCartao($(this).val());
    });

    function fetchDataAndUpdateFieldsCartao(pk) {
        let url = `/inicio/autocomplete/usuario-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_usuario_desc_cartao").val(data.username);
        });
    }

    function initializeAutocompleteCred() {
        $("#dado_usuario_desc_cred").autocomplete({
            source: "/inicio/autocomplete/usuario-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_usuario_cred").val(ui.item.pk);
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

    $("#id_usuario_cred").on("change", function() {
        fetchDataAndUpdateFieldsCred($(this).val());
    });

    function fetchDataAndUpdateFieldsCred(pk) {
        let url = `/inicio/autocomplete/usuario-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_usuario_desc_cred").val(data.username);
        });
    }

    function initializeAutocompleteCons() {
        $("#dado_usuario_desc_cons").autocomplete({
            source: "/inicio/autocomplete/usuario-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_usuario_cons").val(ui.item.pk);
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

    $("#id_usuario_cons").on("change", function() {
        fetchDataAndUpdateFieldsCons($(this).val());
    });

    function fetchDataAndUpdateFieldsCons(pk) {
        let url = `/inicio/autocomplete/usuario-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_usuario_desc_cons").val(data.username);
        });
    }

    function initializeAutocompleteRel() {
        $("#dado_usuario_desc_rel").autocomplete({
            source: "/inicio/autocomplete/usuario-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_usuario_rel").val(ui.item.pk);
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

    $("#id_usuario_rel").on("change", function() {
        fetchDataAndUpdateFieldsRel($(this).val());
    });

    function fetchDataAndUpdateFieldsRel(pk) {
        let url = `/inicio/autocomplete/usuario-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_usuario_desc_rel").val(data.username);
        });
    }

});

