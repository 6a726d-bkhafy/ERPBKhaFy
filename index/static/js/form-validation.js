document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const successMessage = urlParams.get('success');

    if (successMessage) {
        const successContainer = document.getElementById('success-container');
        successContainer.innerHTML = '<strong>Sucesso!</strong><ul>';
        successContainer.innerHTML += `<li>${successMessage}</li>`;
        successContainer.innerHTML += '</ul>';
        successContainer.style.display = 'block';
    }
});


function enviarFormulario(formularioId) {
    const form = document.getElementById(formularioId);
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.concluido) {

            if (data.nf) {
                window.location.href = data.nf;
            }

            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                const currentUrlParams = new URLSearchParams(window.location.search);
                currentUrlParams.set('success', data.success);
                window.location.replace(`${window.location.pathname}?${currentUrlParams.toString()}`);
            }

        } else {
            
            const successContainer = document.getElementById('success-container');
            successContainer.style.display = 'none';

            const errorContainer = document.getElementById('error-container');
            errorContainer.innerHTML = '<strong>A operação não pôde ser realizada devido ao seguinte erro:</strong><ul>';
            for (const field in data.erros) {
                errorContainer.innerHTML += `<li>${data.erros[field]}</li>`;
            }
            errorContainer.innerHTML += '</ul>';
            errorContainer.style.display = 'block';

            $(`#${formularioId}`).closest('.modal').modal('hide');

            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    })
    .catch(error => {
        console.error(error);
    });
}

function enviarFormularioPDF(formularioId) {
    const form = document.getElementById(formularioId);
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.concluido) {
            window.open(data.pdf_path, '_blank');
            window.location.replace(window.location.href.split('?')[0]);
        } else {
            const successContainer = document.getElementById('success-container');
            successContainer.style.display = 'none';

            const errorContainer = document.getElementById('error-container');
            errorContainer.innerHTML = '<strong>A operação não pôde ser realizada devido ao seguinte erro:</strong><ul>';
            for (const field in data.erros) {
                errorContainer.innerHTML += `<li>${data.erros[field]}</li>`;
            }
            errorContainer.innerHTML += '</ul>';
            errorContainer.style.display = 'block';

            $(`#${formularioId}`).closest('.modal').modal('hide');

            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    })
    .catch(error => {
        console.error(error);
    });
}

function imprimirNotaFiscal() {
    
    window.location.href = 'websys:teste';
}

function criarNotaFiscal() {
    
    const notaFiscalHTML = `
        <!DOCTYPE html>
        <html>
            <head>
                <title>Nota Fiscal</title>
        
                <style>
                    #corpo {
                        width: 380px;
                        font-family: sans-serif;
                        font-weight: bold;
                        font-size: 13px;
                    }
                    .between {
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 10px;
                    }
                    .center {
                        display: flex;
                        justify-content: center;
                        margin-bottom: 10px;
                    }
                    .left {
                        display: flex;
                        justify-content: left;
                        margin-bottom: 10px;
                    }
                    label {
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                    }
                </style>
        
            </head>
            <body>
                <div id="corpo">
                    <div class="center">
                        <label>==================================================</label>
                    </div>
                    <div class="between">
                        <label>DD/MM/AAAA</label>
                        <label>HH:MM</label>
                    </div>
                    <div class="center">
                        <label>SAVANA STORE</label>
                    </div>
                    <div class="center">
                        <label>RUA PROF. FRANCISCO ASSIS MADEIRA, 471</label>
                    </div>
                    <div class="center">
                        <label>FONE (15) 2108-1470</label>
                    </div>
                    <div class="center">
                        <label>&lt;CUPOM SEM VALOR FISCAL&gt;</label>
                    </div>
                    <div class="center">
                        <label>---------------------------------------------------------------------------------------</label>
                    </div>
                    <div class="left">
                        <label>CLIENTE: 00001 | CLIENTE TESTE 1</label>
                    </div>
                    <br>
                    <div class="left">
                        <label>TIPO PAGAMENTO: CREDIARIO | PARCELAS: 3</label>
                    </div>
                    <div class="left">
                        <label>VENCIMENTOS:</label>
                    </div>
                    <div class="between">
                        <label>DD/MM/AAAA</label>
                        <label>VLR:  R$ 66,66</label>
                    </div>
                    <div class="between">
                        <label>DD/MM/AAAA</label>
                        <label>VLR:  R$ 66,66</label>
                    </div>
                    <div class="between">
                        <label>DD/MM/AAAA</label>
                        <label>VLR:  R$ 66,66</label>
                    </div>
                    <div class="center">
                        <label>---------------------------------------------------------------------------------------</label>
                    </div>
                    <div class="left">
                        <label>CODIGO | DESCRICAO</label>
                    </div>
                    <div class="center">
                        <label>QTDE x R$ UND | R$ DESC | R$ VLR</label>
                    </div>
                    <div class="center">
                        <label>---------------------------------------------------------------------------------------</label>
                    </div>
                    <div class="left">
                        <label>000001 | PRODUTO TESTE PARA TESTAR IMPRESSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</label>
                    </div>
                    <div class="center">
                        <label>2 x R$ 50,00 | R$ 0,00 | R$ 100,00</label>
                    </div>
                    <div class="left">
                        <label>000002 | PRODUTO TESTE PARA TESTAR OUTRA I</label>
                    </div>
                    <div class="center">
                        <label>1 x R$ 110,00 | R$ 10,00 | R$ 100,00</label>
                    </div>
                    <div class="center">
                        <label>---------------------------------------------------------------------------------------</label>
                    </div>
                    <div class="between">
                        <label>Sub Total:</label>
                        <label>R$ 210,00</label>
                    </div>
                    <div class="between">
                        <label>Desconto:</label>
                        <label>R$ 10,00</label>
                    </div>
                    <div class="between">
                        <label>Total Geral:</label>
                        <label>R$ 200,00</label>
                    </div>
                    <br>
                    <div class="between">
                        <label>Valor Pago:</label>
                        <label>R$ 200,00</label>
                    </div>
                    <div class="between">
                        <label>Troco:</label>
                        <label>R$ 0,00</label>
                    </div>
                    <div class="center">
                        <label>---------------------------------------------------------------------------------------</label>
                    </div>
                    <div class="left">
                        <label>VENDEDOR: 2 | TATA</label>
                    </div>
                    <div class="center">
                        <label>---------------------------------------------------------------------------------------</label>
                    </div>
                    <div class="center">
                        <label>&lt;TROCA SOMENTE COM APRESENTACAO DESTE&gt;</label>
                    </div>
                    <div class="center">
                        <label>&lt;VOLTE SEMPRE&gt;</label>
                    </div>
                    <div class="center">
                        <label>==================================================</label>
                    </div>
                </div>
            </body>
        </html>
    `;

    return notaFiscalHTML;
}