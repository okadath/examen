import pytest
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def product():
    return Product.objects.create(id=55,sku='test_sku', name='Test Product', stock=10)

@pytest.mark.django_db
def test_update_stock_success(api_client, product):
    url = f'/api/inventories/product/{product.id}'
    data = {'amount': 5}
    response = api_client.patch(url, data, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Order received'
    product.refresh_from_db()
    assert product.stock == 15

@pytest.mark.django_db
def test_update_stock_product_not_found(api_client):
    url = '/api/inventories/product/9999' 
    data = {'amount': 5}
    response = api_client.patch(url, data, format='json')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == 'Product not found'

@pytest.mark.django_db
def test_update_stock_invalid_amount(api_client, product):
    url = f'/api/inventories/product/{product.id}'
    data = {'amount': -5}
    response = api_client.patch(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'non_field_errors' in response.data
    assert response.data['non_field_errors'][0] == 'Quantity must be a positive integer.'

@pytest.mark.django_db
def test_update_stock_missing_amount(api_client, product):
    url = f'/api/inventories/product/{product.id}'
    data = {}
    response = api_client.patch(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'amount' in response.data
    assert response.data['amount'][0] == 'This field is required.'
