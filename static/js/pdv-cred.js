let dadoParcela;
let dadoValorParcela;
let dadoTotal;

document.addEventListener('DOMContentLoaded', function(){

    dadoParcela = document.getElementById('dado_parcela');
    dadoValorParcela = document.getElementById('dado_valor_parcela');
    dadoTotal = document.getElementById('dado_total_cred');
});

function handleInputChangeCred() {

    let dadoParcelaInt = parseInt(dadoParcela.value);
    let dadoTotalText = dadoTotal.innerText.split("R$ ")[1];
    let dadoTotalFloat = parseFloat(dadoTotalText);

    let dadoValorParcelaFloat = dadoTotalFloat / dadoParcelaInt;

    let displayValue = isNaN(dadoValorParcelaFloat) ? 0 : dadoValorParcelaFloat.toFixed(2);
    dadoValorParcela.innerText = 'R$ ' + displayValue;
}