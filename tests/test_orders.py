import pytest
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_products(db):  
    Product.objects.create(sku="1", stock=15)
    Product.objects.create(sku="2", stock=5)


@pytest.mark.django_db
def test_order_quantity_positive(api_client, create_products):
    response = api_client.post('/api/orders', {
        "products": [
            {"sku": "1", "quantity": 10},
            {"sku": "2", "quantity": 2}
        ]
    }, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Order received"


@pytest.mark.django_db
def test_order_quantity_zero(api_client, create_products):
    response = api_client.post('/api/orders', {
        "products": [
            {"sku": "1", "quantity": 0}
        ]
    }, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Quantity must be a positive integer." in str(response.data)

@pytest.mark.django_db
def test_order_sku_does_not_exist(api_client):
    response = api_client.post('/api/orders', {
        "products": [
            {"sku": "999", "quantity": 10}
        ]
    }, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "SKU 999 does not exist." in str(response.data)

@pytest.mark.django_db
def test_order_quantity_exceeds_stock(api_client, create_products):
    response = api_client.post('/api/orders', {
        "products": [
            {"sku": "1", "quantity": 20}
        ]
    }, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Quantity 20 exceeds stock 15 for SKU 1." in str(response.data)