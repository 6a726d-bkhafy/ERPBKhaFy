function handleInputChange(pk) {

    let valorPago = parseFloat(document.getElementById(`dado_valor_pago${pk}`).value) || 0;
    let valorTotal = parseFloat(document.getElementById(`dado_total_value${pk}`).value);
    let trocoTotal = document.getElementById(`dado_troco${pk}`);

    let troco = valorPago - valorTotal;
    if (troco < 0) troco = 0;

    trocoTotal.innerText = 'R$ ' + troco.toFixed(2);
}