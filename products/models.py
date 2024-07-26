from django.db import models

# Create your models here.
class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    stock= models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.sku+"-"+self.name+"-"+str(self.stock)