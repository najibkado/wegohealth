from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=255)

class Client(models.Model):
    name = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    lga = models.CharField(max_length=255)
    ward = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

class Questionaire(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    have_account = models.BooleanField(default=False)
    loan_access = models.BooleanField(default=False)
    financial_support = models.BooleanField(default=False)
    max_loan = models.CharField(max_length=255)
    business_experience = models.CharField(max_length=255)
    shop_experience = models.CharField(max_length=255)
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

class Kyc(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    passport_name = models.CharField(max_length=50)
    outter_name = models.CharField(max_length=50)
    inner_name = models.CharField(max_length=50)
    client_Passport_Img = models.ImageField(upload_to='images/')
    client_Outter_Img = models.ImageField(upload_to='images/')
    client_Inner_Img = models.ImageField(upload_to='images/')

class Shop(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    kyc = models.ForeignKey(Kyc, on_delete=models.CASCADE)
    wego_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    addr = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

class Drug(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="owner")
    drug = models.CharField(max_length=255)
    quantity = models.IntegerField()
    approved = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
