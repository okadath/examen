from django.contrib import admin

# Register your models here.
from .models import Product

@admin.register(Product)
class ProductoAdmin(admin.ModelAdmin):
    pass