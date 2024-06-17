from django.db import models
from cfg.models import CTBCATPROD
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from parceiros.models import TBCLI
from .lists import Lists

class TBPROD(models.Model):

    dsc = models.CharField(max_length = 50)
    qtdestoque = models.IntegerField(default = 0)
    qtdcsg = models.IntegerField(default = 0)
    qtdvstg = models.IntegerField(default = 0)
    fk_ctbcatprod = models.ForeignKey(CTBCATPROD, on_delete = models.CASCADE)
    tam = models.CharField(max_length = 10)
    dvlrcusto = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    dvlrvenda = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    qtdmin = models.IntegerField()
    ncm = models.CharField(max_length = 50, null = True, blank = True)
    pvlrmmin = models.DecimalField(max_digits = 10, decimal_places = 2)
    pvlrmatual = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    img = models.ImageField(upload_to = 'produto', default = 'produto/default.png')

    class Meta:

        db_table = 'tbprod'
        permissions = [('view_produtos', 'View Produtos')]

    def clean(self):

        if self.dvlrvenda < (self.dvlrcusto + (self.dvlrcusto * self.pvlrmmin / 100)):
            raise ValidationError('Preço de venda não pode ter valor abaixo da margem mínima!')
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class STBPPROD(models.Model):

    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    qtd = models.IntegerField()
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:

        db_table = 'stbpprod'
        permissions = [('view_etiquetas', 'View Etiquetas')]

class STBIINV(models.Model):

    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    qtdcont = models.IntegerField()
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:

        db_table = 'stbiinv'

class TBINV(models.Model):

    dt = models.DateTimeField()
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:

        db_table = 'tbinv'
        permissions = [('view_inventarios', 'View Inventarios')]

class TBDIFINV(models.Model):

    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    fk_tbinv = models.ForeignKey(TBINV, on_delete = models.CASCADE)
    qtdcont = models.IntegerField()
    qtdestoque = models.IntegerField()
    dif = models.IntegerField()

    class Meta:

        db_table = 'tbdifinv'

class TBCSG(models.Model):

    fk_tbcli = models.ForeignKey(TBCLI, on_delete = models.CASCADE)
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)
    qtd = models.IntegerField()
    dtinicio = models.DateTimeField()
    dtfim = models.DateTimeField()
    sts = models.CharField(max_length = 20, choices = Lists.list_status_consignado)
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:

        db_table = 'tbcsg'
        permissions = [('view_consignado', 'View Consignado')]

    def clean(self):

        if self.fk_tbcli.consdisp < self.dvlr:
            raise ValidationError('Cliente não tem limite disponível suficiente para realizar esse consignado!')
        
        if self.fk_tbcli.clientetrav == True:
            raise ValidationError('Cliente se encontra travado e não pode abrir novos consignados!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class STBOCSG(models.Model):

    qtdtotal = models.IntegerField(null = True, blank = True)
    qtd = models.IntegerField()
    dvlrtotal = models.DecimalField(max_digits = 10, decimal_places = 2)
    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    pvlrdesc = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    fk_tbcsg = models.ForeignKey(TBCSG, on_delete = models.CASCADE)
    estoque = models.BooleanField()
    sts = models.CharField(max_length = 20, choices = Lists.list_status_consignado_venda)
    sel = models.BooleanField(default = True)
    dvlrund = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:

        db_table = 'stbocsg'

class TBIOCSG(models.Model):

    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    fk_tbcsg = models.ForeignKey(TBCSG, on_delete = models.CASCADE)
    qtd = models.IntegerField()
    sts = models.CharField(max_length = 20, choices = Lists.list_status_consignado_venda)
    estoque = models.BooleanField()

    class Meta:

        db_table = 'tbiocsg'