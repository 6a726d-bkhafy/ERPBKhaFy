from django.db import models
from django.core.exceptions import ValidationError
from .lists import Lists
from django.contrib.auth.models import User

class TBCLI(models.Model):

    dsc = models.CharField(max_length = 50)
    doc = models.CharField(max_length = 50, unique = True, error_messages = {'unique': 'Cliente com esse CPF/CNPJ já cadastrado!'})
    rg = models.CharField(max_length = 50, null = True, blank = True)
    tipocli = models.CharField(max_length = 20, choices = Lists.list_tipo_cli)
    dtcad = models.DateTimeField()
    dttrab = models.DateTimeField(null = True, blank = True)
    localtrab = models.CharField(max_length = 50, null = True, blank = True)
    dtnasc = models.DateTimeField(null = True, blank = True)
    ref1 = models.CharField(max_length = 50, null = True, blank = True)
    ref2 = models.CharField(max_length = 50, null = True, blank = True)
    ref3 = models.CharField(max_length = 50, null = True, blank = True)
    num = models.CharField(max_length = 20, null = True, blank = True)
    rua = models.CharField(max_length = 50, null = True, blank = True)
    bairro = models.CharField(max_length = 50, null = True, blank = True)
    cidade = models.CharField(max_length = 50, null = True, blank = True)
    estado = models.CharField(max_length = 50, choices = Lists.list_estados, null = True, blank = True)
    tel1 = models.CharField(max_length = 50, null = True, blank = True)
    tel2 = models.CharField(max_length = 50, null = True, blank = True)
    telrec = models.CharField(max_length = 50, null = True, blank = True)
    teltrab = models.CharField(max_length = 50, null = True, blank = True)
    celular = models.CharField(max_length = 50, null = True, blank = True)
    fan = models.CharField(max_length = 50, null = True, blank = True)
    contato = models.CharField(max_length = 50, null = True, blank = True)
    email = models.CharField(max_length = 50, null = True, blank = True)
    limite = models.DecimalField(max_digits = 10, decimal_places = 2)
    consdisp = models.DecimalField(max_digits = 10, decimal_places = 2)
    creddisp = models.DecimalField(max_digits = 10, decimal_places = 2)
    clientetrav = models.BooleanField(default = False)
    obs = models.CharField(max_length = 300, null = True, blank = True)
    img = models.ImageField(upload_to = 'cliente', default = 'cliente/default.png')

    class Meta:

        db_table = 'tbcli'
        permissions = [('view_clientes', 'View Clientes')]
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBFORN(models.Model):

    razao = models.CharField(max_length = 50)
    doc = models.CharField(max_length = 50, unique = True, error_messages = {'unique': 'Fornecedor com esse CPF/CNPJ já cadastrado!'})
    num = models.CharField(max_length = 20, null = True, blank = True)
    rua = models.CharField(max_length = 50, null = True, blank = True)
    bairro = models.CharField(max_length = 50, null = True, blank = True)
    cidade = models.CharField(max_length = 50, null = True, blank = True)
    estado = models.CharField(max_length = 50, choices = Lists.list_estados, null = True, blank = True)
    tel = models.CharField(max_length = 20, null = True, blank = True)
    email = models.CharField(max_length = 50, null = True, blank = True)

    class Meta:

        db_table = 'tbforn'
        permissions = [('view_fornecedores', 'View Fornecedores')]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBAGENDACLI(models.Model):

    assunto = models.CharField(max_length = 50)
    dsc = models.CharField(max_length = 300, null = True, blank = True)
    tipocontatocli = models.CharField(max_length = 20, choices = Lists.list_tipo_contato)
    dthr = models.DateTimeField()
    resp = models.CharField(max_length = 50, null = True, blank = True)
    stsagendacli = models.CharField(max_length = 20, choices = Lists.list_sts_agenda)
    fk_tbcli = models.ForeignKey(TBCLI, on_delete = models.CASCADE)
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:

        db_table = 'tbagendacli'
        permissions = [('view_agenda_clientes', 'View Agenda Clientes')]
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBAGENDAFORN(models.Model):

    assunto = models.CharField(max_length = 50)
    dsc = models.CharField(max_length = 300, null = True, blank = True)
    tipocontatoforn = models.CharField(max_length = 20, choices = Lists.list_tipo_contato)
    dthr = models.DateTimeField()
    resp = models.CharField(max_length = 50, null = True, blank = True)
    stsagendaforn = models.CharField(max_length = 20, choices = Lists.list_sts_agenda)
    fk_tbforn = models.ForeignKey(TBFORN, on_delete = models.CASCADE)
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:

        db_table = 'tbagendaforn'
        permissions = [('view_agenda_forn', 'View Agenda Forn')]
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
