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
    kyc = models.ForeignKey(Kyc, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    addr = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

class Drug(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="owner")
    drug = models.CharField(max_length=255)
    quantity = models.IntegerField()
    approved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)