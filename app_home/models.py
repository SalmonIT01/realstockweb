from django.db import models

# Create your models here.

class Details(models.Model):
    product_id = models.CharField(max_length = 30, default = '', null = False,unique=True)
    product_name = models.CharField(max_length = 225, default = '', null = False)
    unit = models.ForeignKey('Unit', on_delete=models.SET_NULL, null = True)
    amount = models.FloatField(max_length = 20, default = '', null = False)
    status_id = models.IntegerField(max_length = 20, default = '', null = True)

class Unit(models.Model):
    unit_id = models.IntegerField(max_length = 20, default = '', null = False)
    unit_name = models.CharField(max_length = 225, default = '', null = False)    

# class Borrow(models.Model):
#     b_productid = models.ForeignKey('Details',null = False,on_delete=models.CASCADE)
#     b_amount = models.FloatField(max_length = 20, default = '', null = False)
#     borrow_date = models.DateField(auto_now=False, auto_now_add=False)
#     return_date = models.DateField(auto_now=False, auto_now_add=False ,null=True)
    
class logDetails(models.Model):
    time = models.CharField(max_length = 225, default = '', null = False)
    descri = models.CharField(max_length = 225, default = '', null = False)

class Member(models.Model):
    username = models.CharField(max_length = 225, default = '', null = False)
    password = models.CharField(max_length = 225, default = '', null = False)
