class Lists:

    list_status = (
        ('0', 'Pendente'),
        ('1', 'Pago'),
        ('2', 'Parcialmente Pago'),
        ('3', 'Estornado'),
        ('4', 'Pendente')
    )

    list_tipopg = (
        ('0', 'PIX'),
        ('1', 'Cartão de Crédito'),
        ('2', 'Cartão de Débito'),
        ('3', 'Boleto à Vista'),
        ('4', 'Boleto 30 / 60 / 90'),
        ('5', 'Dinheiro'),
        ('6', 'Crediário'),
        ('7', 'Cheque')
    )

    list_status_caixa = (
        ('0', 'Vendido'),
        ('1', 'Trocado'),
        ('2', 'Em Troca'),
        ('3', 'Venda Troca'),
        ('4', 'Estornado'),
        ('5', 'Vendido sem Estoque')
    )

    list_status_troca = (
        ('0', 'Pendente'),
        ('1', 'Encerrado'),
        ('2', 'Trocado'),
        ('3', 'Vendido')
    )

    list_tipop = (
        ('1', 'Entrada NF + Estoque'),
        ('2', 'Entrada Estoque'),
        ('3', 'Entrada NF'),
        ('4', 'Saída Estoque'),
        ('5', 'Saída NF')
    )

    list_status_pg = (
        ('0', 'Pago'),
        ('1', 'Estornado')
    )