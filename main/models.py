from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

class Shop(models.Model):
    name = models.CharField(max_length=255)
    addr = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

class Drug(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="owner")
    drug = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)