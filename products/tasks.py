from celery import shared_task
from .models import Product
from datetime import datetime

@shared_task
def check_product_stock():
    low_stock_products = Product.objects.filter(stock__lt=10)
    for product in low_stock_products:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        message = f"[{timestamp}] Product {product.name} (SKU: {product.sku}) has low stock: {product.stock} units."
        print(message)
        with open('low_stock_alerts.txt', 'a') as f:
            f.write(message + '\n')