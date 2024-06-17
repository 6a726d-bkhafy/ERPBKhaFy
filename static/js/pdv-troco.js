let dadoValorInput;
let trocoElement;
let totalValorElement;
let totalDinheiroElement;
let totalCartaoElement;
let descontoDinheiroElement;
let descontoCartaoElement;

document.addEventListener('DOMContentLoaded', function() {

    dadoValorInput = document.getElementById('dado_valor_pago');
    trocoElement = document.getElementById('dado_troco');
    totalValorElement = document.getElementById('dado_total_value');
    totalDinheiroElement = document.getElementById('dado_total_dinheiro');
    totalCartaoElement = document.getElementById('dado_total_cartao');
    descontoDinheiroElement = document.getElementById('dado_desconto_dinheiro');
    descontoCartaoElement = document.getElementById('dado_desconto_cartao');
    
});

function handleInputChange() {

    let valorPago = parseFloat(dadoValorInput.value) || 0;
    let valorTotal = parseFloat(totalValorElement.value);
    let valorDescontoDinheiro = parseFloat(descontoDinheiroElement.value) || 0;
    let valorDescontoCartao = parseFloat(descontoCartaoElement.value) || 0;

    let totalDinheiro = valorTotal - valorDescontoDinheiro
    let totalCartao = valorTotal - valorDescontoCartao

    let troco = valorPago - totalDinheiro;
    if (troco < 0) troco = 0;

    trocoElement.innerText = 'R$ ' + troco.toFixed(2);
    totalDinheiroElement.innerText = 'R$ ' + totalDinheiro.toFixed(2);
    totalCartaoElement.innerText = 'R$ ' + totalCartao.toFixed(2);
    dadoValorInput.min = totalDinheiro.toFixed(2)
}