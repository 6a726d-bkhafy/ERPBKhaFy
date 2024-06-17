let tipoPGInputs;
let contaInputs;
let contaTitles;

document.addEventListener('DOMContentLoaded', function() {

    tipoPGInputs = document.getElementsByClassName('input-tipopg');
    contaInputs = document.getElementsByClassName('input-conta');
    contaTitles = document.getElementsByClassName('title-conta');

    for (let i = 0; i < tipoPGInputs.length; i++) {
        tipoPGInputs[i].addEventListener('input', function() {
            updateContaVisibility(i);
        });
    }

});

function updateContaVisibility(index) {
    if (tipoPGInputs[index].value == "5") {
        contaInputs[index].style.display = 'none';
        contaTitles[index].style.display = 'none';
        contaInputs[index].removeAttribute('required');
    } else {
        contaInputs[index].style.display = 'block';
        contaTitles[index].style.display = 'block';
        contaInputs[index].setAttribute('required', true);
    }
}