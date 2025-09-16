from django.db import models

# Create your models here.


class User(models.Model):
    tg_user=models.CharField(max_length=300)
    user_ismi = models.CharField(max_length=300)
    balans = models.CharField(max_length=300)
    til = models.CharField(max_length=300)


class summa(models.Model):
    summa=models.CharField(max_length=300)




class Admin(models.Model):
    tg_user = models.CharField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=300, blank=True, null=True)
    ismi = models.CharField(max_length=300, blank=True, null=True)

class kanallar(models.Model):
    tg_user = models.CharField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=300, blank=True, null=True)
    ismi = models.CharField(max_length=300, blank=True, null=True)




class shablon_kurs(models.Model):
    tg_id= models.CharField(max_length=300, blank=True, null=True)
    institut = models.CharField(max_length=300, blank=True, null=True)
    ism_fam = models.CharField(max_length=300, blank=True, null=True)
    sahifa_soni= models.CharField(max_length=300, blank=True, null=True)
    til= models.CharField(max_length=300, blank=True, null=True)
    kurs_tili=models.CharField(max_length=300, blank=True, null=True)

class shablon_pre(models.Model):
    tg_id= models.CharField(max_length=300, blank=True, null=True)
    bg_num=models.CharField(max_length=300, blank=True, null=True)
    ism_fam = models.CharField(max_length=300, blank=True, null=True)
    til= models.CharField(max_length=300, blank=True, null=True)
    slayid_soni=models.CharField(max_length=300, blank=True, null=True)
    pre_tili=models.CharField(max_length=300, blank=True, null=True)


from django.db import models

class Referal(models.Model):
    user_id = models.CharField(max_length=300, unique=True)
    referal_id = models.CharField(max_length=300, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user_id} - balance: {self.balance}"