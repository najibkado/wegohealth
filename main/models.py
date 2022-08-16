from django.db import models

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    addr = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

class Drug(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="owner")
    drug = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)