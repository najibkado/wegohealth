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

class Questionaire(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    is_business_owner = models.BooleanField(default=False)
    duration = models.CharField(max_length=255)
    delivery = models.CharField(max_length=255)
    commute = models.CharField(max_length=255)
    challenges = models.CharField(max_length=255)
    credit = models.CharField(max_length=255)
    debtors = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    employees = models.CharField(max_length=255)
    turnover = models.CharField(max_length=255)
    sales = models.CharField(max_length=255)
    cac = models.BooleanField(default=False)
    council = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

class Shop(models.Model):
    name = models.CharField(max_length=255)
    addr = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

class Drug(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="owner")
    drug = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)