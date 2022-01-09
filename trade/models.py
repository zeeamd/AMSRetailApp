from django.db import models
from datetime import datetime

class Brand(models.Model):
    bname = models.CharField(max_length=10, unique=True)

class Product(models.Model):
    class Meta:
        unique_together = (('bname','name','size'),)
    bname = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    size = models.CharField(max_length=10)
    quantity = models.IntegerField(default=0)

class Purchase(models.Model):
    pp = models.ForeignKey(Product, on_delete=models.CASCADE)
    pdate = models.DateTimeField(auto_now=True)
    prate = models.FloatField(default=0.0)
    pquantity = models.IntegerField(default=0)
    pnotes = models.CharField(max_length=1000)

class Sale(models.Model):
    sp = models.ForeignKey(Product, on_delete=models.CASCADE)
    to_customer = models.CharField(max_length=20)
    sdate = models.DateTimeField(auto_now=True)
    srate = models.FloatField(default=0.0)
    squantity = models.IntegerField(default=0)
    discounttype = models.CharField(max_length=10)
    discount = models.FloatField(default=0.0)
    sprice = models.FloatField(default=0.0)

class Credit(models.Model):
    cdate = models.DateTimeField(auto_now=True)
    ccustomer = models.CharField(max_length=20)
    camount = models.FloatField(default=0.0)
