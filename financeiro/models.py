from django.db import models
from parceiros.models import TBFORN, TBCLI
from cfg.models import CTBCATFIN, CTBBANK, CTBITIPOPG
from django.core.exceptions import ValidationError
from .lists import Lists
from estoque.models import TBPROD
from django.contrib.auth.models import User
from compras.models import TBCOMP
from datetime import datetime

class TBIOCX(models.Model):

    sts = models.IntegerField()
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:

        db_table = 'tbiocx'

    def clean(self):

        caixa = TBIOCX.objects.latest('pk')

        if self.dvlr < 0:
            raise ValidationError('Valor em caixa insuficiente para essa operação!')
        
        if caixa.sts == 0 and self.sts == 0 and caixa.dvlr != self.dvlr:
            raise ValidationError('Caixa está fechado e não pode realizar transações!')
        
        if self != caixa and caixa.sts == 1:
            raise ValidationError('Operação bloqueada por referenciar caixa já encerrado!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBCX(models.Model):

    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)
    fk_ctbitipopg = models.ForeignKey(CTBITIPOPG, on_delete = models.CASCADE, null = True, blank = True)
    qtdparc = models.IntegerField()
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)
    fk_tbcli = models.ForeignKey(TBCLI, on_delete = models.CASCADE)
    dt = models.DateTimeField()
    sts = models.CharField(max_length = 20, choices = Lists.list_status_caixa)
    crediario = models.IntegerField(null = True, blank = True)

    class Meta:

        db_table = 'tbcx'
        permissions = [('view_caixa', 'View Caixa')]

    def clean(self):

        if self.fk_tbcli.creddisp < self.dvlr and self.qtdparc > 1 and self.sts != '4':
            raise ValidationError('Cliente não tem limite disponível suficiente para realizar esse crediário!')
        
        if self.qtdparc > 1 and self.fk_tbcli.clientetrav == True and self.sts != '4':
            raise ValidationError('Cliente se encontra travado e não pode abrir novos crediários!')
        
        if self.sts == '4' and self.qtdparc > 1:
            
            pgs = TBIPG.objects.filter(fk_tbcx = self, sts = '0')
            if pgs:
                raise ValidationError('Essa movimentação possui recebimentos!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBICRED(models.Model):

    fk_tbcx = models.ForeignKey(TBCX, on_delete = models.CASCADE)
    qtdparc = models.IntegerField()
    qtdpaga = models.IntegerField()
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:

        db_table = 'tbicred'

    def clean(self):

        cred = TBICRED.objects.filter(pk = self.pk)
        
        if cred:
            if cred[0].dvlr != self.dvlr:
                raise ValidationError(f'A soma de todas as parcelas deve corresponder a R$ {cred[0].dvlr}, porém resulta em R$ {self.dvlr}!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBOFIN(models.Model):

    fk_tbforn = models.ForeignKey(TBFORN, on_delete = models.CASCADE, null = True, blank = True)
    dvlrtotal = models.DecimalField(max_digits = 10, decimal_places = 2)
    dvlrpend = models.DecimalField(max_digits = 10, decimal_places = 2)
    fk_ctbcatfin = models.ForeignKey(CTBCATFIN, on_delete = models.CASCADE, null = True, blank = True)
    dtem = models.DateTimeField()
    dtvenc = models.DateTimeField()
    sts = models.CharField(max_length = 20, choices = Lists.list_status)
    tipoop = models.CharField(max_length = 20, choices = Lists.list_tipop)
    comprod = models.BooleanField()
    dsc = models.CharField(max_length = 100, null = True, blank = True)
    boleto = models.FileField(upload_to = 'financeiro', null = True, blank = True)
    numnota= models.IntegerField()
    fk_tbcomp = models.ForeignKey(TBCOMP, on_delete = models.CASCADE, null = True, blank = True)

    class Meta:

        db_table = 'tbofin'
        permissions = [('view_saida', 'View Saida')]

    def clean(self):

        if self.dtem > self.dtvenc:
            raise ValidationError('Data de emissão não pode ser maior que data de vencimento!')
        
        if self.boleto and self.boleto.size > 500000:
            raise ValidationError('Arquivo excede o limite de 500 KB!')

        if self.sts == '3':
            
            pgs = TBOPG.objects.filter(fk_tbofin = self, sts = '0')
            if pgs:
                raise ValidationError('Esse lançamento possui pagamentos!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBIFIN(models.Model):

    fk_tbcli = models.ForeignKey(TBCLI, on_delete = models.CASCADE, null = True, blank = True)
    dvlrtotal = models.DecimalField(max_digits = 10, decimal_places = 2)
    dvlrpend = models.DecimalField(max_digits = 10, decimal_places = 2)
    dtem = models.DateTimeField()
    dtvenc = models.DateTimeField()
    sts = models.CharField(max_length = 20, choices = Lists.list_status)
    tipoop = models.IntegerField()
    numnota = models.IntegerField(null = True, blank = True)
    fk_tbicred = models.ForeignKey(TBICRED, on_delete = models.CASCADE, null = True, blank = True)
    fk_tbcx = models.ForeignKey(TBCX, on_delete = models.CASCADE, null = True, blank = True)

    class Meta:

        db_table = 'tbifin'
        permissions = [('view_entrada', 'View Entrada')]

class TBOPG(models.Model):

    fk_tbofin = models.ForeignKey(TBOFIN, on_delete = models.CASCADE)
    dtpg = models.DateTimeField()
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)
    fk_ctbbank = models.ForeignKey(CTBBANK, on_delete = models.CASCADE, null = True, blank = True)
    tipopg = models.CharField(max_length = 20, choices = Lists.list_tipopg)
    fk_tbiocx = models.ForeignKey(TBIOCX, on_delete = models.CASCADE, null = True, blank = True)
    sts = models.CharField(max_length = 20, choices = Lists.list_status_pg)

    class Meta:

        db_table = 'tbopg'

    def clean(self):

        if self.dtpg.date() != datetime.now().date():
            raise ValidationError('Apenas é possível realizar estorno no mesmo dia do pagamento!')
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBIPG(models.Model):

    fk_tbifin = models.ForeignKey(TBIFIN, on_delete = models.CASCADE, null = True, blank = True)
    dtpg = models.DateTimeField()
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)
    fk_ctbbank = models.ForeignKey(CTBBANK, on_delete = models.CASCADE, null = True, blank = True)
    fk_ctbitipopg = models.ForeignKey(CTBITIPOPG, on_delete = models.CASCADE, null = True, blank = True)
    fk_tbcx = models.ForeignKey(TBCX, on_delete = models.CASCADE)
    fk_tbiocx = models.ForeignKey(TBIOCX, on_delete = models.CASCADE, null = True, blank = True)
    sts = models.CharField(max_length = 20, choices = Lists.list_status_pg)
    dif = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)

    class Meta:

        db_table = 'tbipg'

    def clean(self):

        if self.dtpg.date() != datetime.now().date():
            raise ValidationError('Apenas é possível realizar estorno no mesmo dia do pagamento!')
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class STBOPROD(models.Model):

    qtd = models.IntegerField()
    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    pvlrdesc = models.DecimalField(max_digits = 10, decimal_places = 2)
    dvlrtotal = models.DecimalField(max_digits = 10, decimal_places = 2)
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)
    estoque = models.BooleanField()
    dvlrund = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:

        db_table = 'stboprod'
        permissions = [('view_pdv', 'View PDV')]

    def clean(self):

        if self.dvlrtotal == 0:
            raise ValidationError('Produto não possuí preço de venda!')
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBTPROD(models.Model):

    fk_tbcx_entrada = models.ForeignKey(TBCX, on_delete = models.CASCADE, related_name = 'fk_tbcx_entrada')
    fk_tbcx_saida = models.ForeignKey(TBCX, on_delete = models.CASCADE, related_name = 'fk_tbcx_saida', null = True, blank = True)
    fk_tbcli = models.ForeignKey(TBCLI, on_delete = models.CASCADE)
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)
    sts = models.CharField(max_length = 20, choices = Lists.list_status_troca)
    dt = models.DateTimeField()

    class Meta:

        db_table = 'tbtprod'
        permissions = [('view_troca', 'View Troca')]

    def clean(self):

        if self.dvlr == 0:
            raise ValidationError('Ordem de troca não pode ser aberta sem produtos!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TBOPROD(models.Model):

    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    qtd = models.IntegerField()
    fk_tbcx = models.ForeignKey(TBCX, on_delete = models.CASCADE)
    tipomov = models.IntegerField()
    sts = models.CharField(max_length = 20, choices = Lists.list_status_caixa)
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)
    fk_tbtprod = models.ForeignKey(TBTPROD, on_delete = models.CASCADE, null = True, blank = True)

    class Meta:

        db_table = 'tboprod'

class TBIOTPROD(models.Model):

    fk_tbtprod = models.ForeignKey(TBTPROD, on_delete = models.CASCADE)
    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)
    qtd = models.IntegerField()
    sts = models.CharField(max_length = 20, choices = Lists.list_status_troca)

    class Meta:

        db_table = 'tbiotprod'

class STBOTPROD(models.Model):

    fk_tbtprod = models.ForeignKey(TBTPROD, on_delete = models.CASCADE)
    fk_tbprod = models.ForeignKey(TBPROD, on_delete = models.CASCADE)
    qtd = models.IntegerField()
    dvlrund = models.DecimalField(max_digits = 10, decimal_places = 2)
    dvlrtotal = models.DecimalField(max_digits = 10, decimal_places = 2)
    pvlrdesc = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    estoque = models.BooleanField()

    class Meta:

        db_table = 'stbotprod'

class TBIOTRANSF(models.Model):

    fk_ctbbank_in = models.ForeignKey(CTBBANK, on_delete = models.CASCADE, related_name = 'fk_ctbbank_in')
    fk_ctbbank_out = models.ForeignKey(CTBBANK, on_delete = models.CASCADE, related_name = 'fk_ctbbank_out')
    dvlr = models.DecimalField(max_digits = 10, decimal_places = 2)
    dt = models.DateTimeField()
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:

        db_table = 'tbiotransf'
        permissions = [('view_transf', 'View Transf')]