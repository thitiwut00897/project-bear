from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    tel = models.CharField(max_length=10,null=True)
    picture = models.ImageField(default='default_pic.png',upload_to='user',null=True,blank=True)
class Type(models.Model):
    type_name = models.CharField(max_length=255)
    def __str__(self):
        return self.type_name
    
class Product(models.Model):
    type = models.ForeignKey(Type, on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255,null=True)
    price = models.FloatField()
    stock = models.IntegerField()
    picture = models.ImageField(upload_to='product_pic',null=True,blank=True)
    def __str__(self):
        return self.name
class Order(models.Model):
    date = models.DateTimeField(auto_now=True)
    total_price = models.FloatField()
class Order_items(models.Model):
    item_no = models.ForeignKey(Product, on_delete=models.PROTECT,null=True)
    unit = models.IntegerField()
    price = models.FloatField()
    item_price = models.FloatField()
class Order_Products(models.Model):
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    user_id = models.IntegerField()
class Payment(models.Model):
    pay_time = models.DateTimeField(auto_now=True)
    pay_price = models.FloatField()