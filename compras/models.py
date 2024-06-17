from django.db import models
from parceiros.models import TBFORN
from django.core.exceptions import ValidationError
from estoque.models import TBPROD
from .lists import Lists
from django.contrib.auth.models import User
from cfg.models import CTBCATFIN

class TBCOMP(models.Model):

    fk_tbforn = models.ForeignKey(TBFORN, on_delete = models.CASCADE)
    sts = models.CharField(max_length = 20, choices = Lists.list_status)
    dt = models.DateTimeField()
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)
    tipomov = models.IntegerField()
    qtd = models.IntegerField()
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)
    fk_ctbcatfin = models.ForeignKey(CTBCATFIN, on_delete = models.CASCADE)
    numnota = models.IntegerField()
    dtvenc = models.DateTimeField()
    dtem = models.DateTimeField()
    qtdparc = models.IntegerField()

    class Meta:

        db_table = 'tbcomp'
        permissions = [('view_compra', 'View Compra')]

class STBICOMP(models.Model):

    fk_tbcomp = models.ForeignKey(TBCOMP, on_delete = models.CASCADE)
    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    qtd = models.IntegerField()
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:

        db_table = 'stbicomp'

    def clean(self):
        
        compra = STBICOMP.objects.filter(fk_tbprod = self.fk_tbprod, fk_tbcomp = self.fk_tbcomp)

        if compra:
            raise ValidationError('Produdo já inserido. Altere a quantidade na aba de opções!')
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBIPROD(models.Model):

    fk_tbcomp = models.ForeignKey(TBCOMP, on_delete = models.CASCADE)
    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    qtd = models.IntegerField()
    qtdpen = models.IntegerField()
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)
    sts = models.CharField(max_length = 20, choices = Lists.list_status_entrada)

    class Meta:

        db_table = 'tbiprod'


class TBLOTE(models.Model):

    sts = models.CharField(max_length = 20, choices = Lists.list_status_lote)
    dt = models.DateTimeField()
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)
    qtd = models.IntegerField()

    class Meta:

        db_table = 'tblote'
        permissions = [('view_lote', 'View Lote')]

class STBILOTE(models.Model):

    fk_tblote = models.ForeignKey(TBLOTE, on_delete = models.CASCADE)
    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    qtd = models.IntegerField()

    class Meta:

        db_table = 'stbilote'

    def clean(self):
        
        lote = STBILOTE.objects.filter(fk_tbprod = self.fk_tbprod, fk_tblote = self.fk_tblote)

        if lote:
            raise ValidationError('Produdo já inserido. Altere a quantidade na aba de opções!')
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBILOTE(models.Model):

    fk_tblote = models.ForeignKey(TBLOTE, on_delete = models.CASCADE)
    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    qtd = models.IntegerField()
    class Meta:

        db_table = 'tbilote'