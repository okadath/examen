from rest_framework import serializers
from products.models import Product

 
class NewProductSerializer(serializers.ModelSerializer):  
    sku = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)

    class Meta:
        model=Product
        fields=[
            "sku",
            "name"
            ]

    def validate(self, data):
        sku = data.get('sku')
        if Product.objects.filter(sku=sku).exists():
            raise serializers.ValidationError(f"A product with SKU {sku} already exists.")
        return data


class AddStockSerializer(serializers.ModelSerializer):  
    amount = serializers.IntegerField()

    class Meta:
        model=Product
        fields=[
            "amount"
            ]

    def validate(self, data): 
        amount = data.get('amount')
        if amount <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return data




class OrderSerializer(serializers.ModelSerializer):  
    sku = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()

    class Meta:
        model=Product
        fields=[
            "sku",
            "quantity"
            ]

    def validate(self, data):
        sku = data.get('sku')
        quantity = data.get('quantity')

        if quantity <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"SKU {sku} does not exist.")
        if quantity > product.stock:
            raise serializers.ValidationError(f"Quantity {quantity} exceeds stock {product.stock} for SKU {sku}.")
        return data


class OrderListSerializer(serializers.ModelSerializer):  
    products = OrderSerializer(many=True)

    class Meta:
        model=Product
        fields=[
            "products"
        ]

