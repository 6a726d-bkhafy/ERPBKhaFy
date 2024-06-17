document.addEventListener('DOMContentLoaded', function() {
    const inputProduto = document.getElementById('id_produto');

    inputProduto.addEventListener('keydown', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();

            if (inputProduto.value) {
                enviarFormulario('formulario');
            }
        }
    });
});