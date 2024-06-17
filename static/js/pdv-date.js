window.onload = function() {
    var today = new Date();
    var day = ("0" + today.getDate()).slice(-2);
    var month = ("0" + (today.getMonth() + 1)).slice(-2);
    var year = today.getFullYear();
    document.getElementById('dado_data_venda').value = day + '/' + month + '/' + year; // Define o valor do campo com a data atual no formato 'dd/mm/aaaa'
};
