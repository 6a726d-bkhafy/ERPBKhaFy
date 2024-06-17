$(document).ready(function() {

    $('#modal-pgdinheiro-venda').on('shown.bs.modal', function() {
        initializeAutocompleteDin();
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

    $('#modal-filter-list-entrada-financeiro').on('shown.bs.modal', function() {
        initializeAutocomplete();
    });

    $('#modal-filter-list-troca').on('shown.bs.modal', function() {
        initializeAutocomplete();
    });

    $('#modal-filter-list-consignado').on('shown.bs.modal', function() {
        initializeAutocomplete();
    });

    $('#modal-relatorio').on('shown.bs.modal', function() {
        initializeAutocompleteRel();
    });

    function initializeAutocomplete() {
        $("#dado_cliente_desc").autocomplete({
            source: "/inicio/autocomplete/cliente-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_cliente").val(ui.item.pk);
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

    $("#id_cliente").on("change", function() {
        fetchDataAndUpdateFields($(this).val());
    });

    function fetchDataAndUpdateFields(pk) {
        let url = `/inicio/autocomplete/cliente-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_cliente_desc").val(data.dsc);
        });
    }

    function initializeAutocompleteCartao() {
        $("#dado_cliente_desc_cartao").autocomplete({
            source: "/inicio/autocomplete/cliente-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_cliente_cartao").val(ui.item.pk);
                $("#dado_pend_cartao").val(ui.item.dvlrpend);
                $("#dado_atraso_cartao").val(ui.item.atraso);
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

    $("#id_cliente_cartao").on("change", function() {
        fetchDataAndUpdateFieldsCartao($(this).val());
    });

    function fetchDataAndUpdateFieldsCartao(pk) {
        let url = `/inicio/autocomplete/cliente-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_cliente_desc_cartao").val(data.dsc);
            $("#dado_pend_cartao").val(data.dvlrpend);
            $("#dado_atraso_cartao").val(data.atraso);
        });
    }

    function initializeAutocompleteCred() {
        $("#dado_cliente_desc_cred").autocomplete({
            source: "/inicio/autocomplete/cliente-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_cliente_cred").val(ui.item.pk);
                $("#dado_limite_cred").val(ui.item.limite);
                $("#dado_disp_cred").val(ui.item.creddisp);
                $("#dado_pend_cred").val(ui.item.dvlrpend);
                $("#dado_atraso_cred").val(ui.item.atraso);
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

    $("#id_cliente_cred").on("change", function() {
        fetchDataAndUpdateFieldsCred($(this).val());
    });

    function fetchDataAndUpdateFieldsCred(pk) {
        let url = `/inicio/autocomplete/cliente-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_cliente_desc_cred").val(data.dsc);
            $("#dado_limite_cred").val(data.limite);
            $("#dado_disp_cred").val(data.creddisp);
            $("#dado_pend_cred").val(data.dvlrpend);
            $("#dado_atraso_cred").val(data.atraso);
        });
    }

    function initializeAutocompleteCons() {
        $("#dado_cliente_desc_cons").autocomplete({
            source: "/inicio/autocomplete/cliente-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_cliente_cons").val(ui.item.pk);
                $("#dado_limite_cons").val(ui.item.limite);
                $("#dado_disp_cons").val(ui.item.consdisp);
                $("#dado_pend_cons").val(ui.item.dvlrpend);
                $("#dado_atraso_cons").val(ui.item.atraso);
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

    $("#id_cliente_cons").on("change", function() {
        fetchDataAndUpdateFieldsCons($(this).val());
    });

    function fetchDataAndUpdateFieldsCons(pk) {
        let url = `/inicio/autocomplete/cliente-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_cliente_desc_cons").val(data.dsc);
            $("#dado_limite_cons").val(data.limite);
            $("#dado_disp_cons").val(data.consdisp);
            $("#dado_pend_cons").val(data.dvlrpend);
            $("#dado_atraso_cons").val(data.atraso);
        });
    }

    function initializeAutocompleteDin() {
        $("#dado_cliente_desc").autocomplete({
            source: "/inicio/autocomplete/cliente-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_cliente").val(ui.item.pk);
                $("#dado_pend_din").val(ui.item.dvlrpend);
                $("#dado_atraso_din").val(ui.item.atraso);
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

    $("#id_cliente").on("change", function() {
        fetchDataAndUpdateFieldsDin($(this).val());
    });

    function fetchDataAndUpdateFieldsDin(pk) {
        let url = `/inicio/autocomplete/cliente-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_cliente_desc").val(data.dsc);
            $("#dado_pend_din").val(data.dvlrpend);
            $("#dado_atraso_din").val(data.atraso);
        });
    }

    function initializeAutocompleteRel() {
        $("#dado_cliente_desc_rel").autocomplete({
            source: "/inicio/autocomplete/cliente-by-desc",
            minLength: 2,
            select: function(event, ui) {
                $("#id_cliente_rel").val(ui.item.pk);
                $("#dado_pend_din").val(ui.item.dvlrpend);
                $("#dado_atraso_din").val(ui.item.atraso);
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

    $("#id_cliente_rel").on("change", function() {
        fetchDataAndUpdateFieldsRel($(this).val());
    });

    function fetchDataAndUpdateFieldsRel(pk) {
        let url = `/inicio/autocomplete/cliente-by-pk/${pk}`;
        $.getJSON(url, function(data) {
            $("#dado_cliente_desc_rel").val(data.dsc);
            $("#dado_pend_din").val(data.dvlrpend);
            $("#dado_atraso_din").val(data.atraso);
        });
    }

});

