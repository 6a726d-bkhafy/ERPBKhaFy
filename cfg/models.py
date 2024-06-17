from django.db import models
from django.contrib.auth.models import User
from .lists import Lists

class CTBPROFILE(models.Model):

    fk_user = models.OneToOneField(User, on_delete = models.CASCADE)
    avatar = models.ImageField(upload_to = 'avatar', default = 'avatar/default.png')

    class Meta:

        db_table = 'ctbprofile'
        permissions = [('view_usuarios', 'View Usuários')]

class CTBCATPROD(models.Model):

    dsc = models.CharField(max_length = 50, unique = True, error_messages = {'unique': 'Categoria já cadastrada!'})

    class Meta:

        db_table = 'ctbcatprod'
        permissions = [('view_categorias', 'View Categorias')]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class CTBCATFIN(models.Model):

    dsc = models.CharField(max_length = 50, unique = True, error_messages = {'unique': 'Tipo de custo já cadastrado!'})

    class Meta:

        db_table = 'ctbcatfin'
        permissions = [('view_custos', 'View Custos')]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class CTBJURO(models.Model):

    pvlr = models.DecimalField(max_digits = 10, decimal_places = 2, unique = True, error_messages = {'unique': 'Porcentagem de juro já cadastrada!'})

    class Meta:

        db_table = 'ctbjuro'
        permissions = [('view_juros', 'View Juros')]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class CTBBANK(models.Model):

    razao = models.CharField(max_length = 50)
    banco = models.CharField(max_length = 50, choices = Lists.list_bancos)
    ag = models.CharField(max_length = 50)
    conta = models.CharField(max_length = 50)
    pix = models.CharField(max_length = 200, null = True, blank = True)
    default = models.BooleanField(default = False)

    class Meta:

        db_table = 'ctbbank'
        permissions = [('view_contas', 'View Contas')]

    def __str__(self):

        return f'{self.razao} / {self.get_banco_display()}'

class CTBITIPOPG(models.Model):

    dsc = models.CharField(max_length = 30)
    fk_ctbbank = models.ForeignKey(CTBBANK, on_delete = models.CASCADE)

    class Meta:

        db_table = 'ctbitipopg'
        permissions = [('view_pagamentos', 'View Pagamentos')]

class CTBEMP(models.Model):

    razao = models.CharField(max_length = 30)
    endereco = models.CharField(max_length = 50)
    tel = models.CharField(max_length = 20)

    class Meta:

        db_table = 'ctbemp'

