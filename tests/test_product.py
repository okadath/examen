import pytest
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def existing_product():
    return Product.objects.create(sku='existing_sku', name='Existing Product')

@pytest.mark.django_db
def test_create_product_success(api_client):
    url = '/api/products'
    data = {
        'sku': 'new_sku',
        'name': 'New Product'
    }
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Product created'
    
    product = Product.objects.get(sku='new_sku')
    assert product.name == 'New Product'

@pytest.mark.django_db
def test_create_product_duplicate_sku(api_client, existing_product):
    url = '/api/products'
    data = {
        'sku': 'existing_sku',
        'name': 'Another Product'
    }
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'non_field_errors' in response.data
    assert response.data['non_field_errors'][0] == 'A product with SKU existing_sku already exists.'

@pytest.mark.django_db
def test_create_product_missing_sku(api_client):
    url = '/api/products'
    data = {
        'name': 'Product Without SKU'
    }
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'sku' in response.data
    assert response.data['sku'][0] == 'This field is required.'

@pytest.mark.django_db
def test_create_product_missing_name(api_client):
    url = '/api/products'
    data = {
        'sku': 'product_without_name'
    }
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data
    assert response.data['name'][0] == 'This field is required.'

@pytest.mark.django_db
def test_create_product_empty_sku(api_client):
    url = '/api/products'
    data = {
        'sku': '',
        'name': 'Product With Empty SKU'
    }
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'sku' in response.data
    assert response.data['sku'][0] == 'This field may not be blank.'

@pytest.mark.django_db
def test_create_product_empty_name(api_client):
    url = '/api/products'
    data = {
        'sku': 'sku_with_empty_name',
        'name': ''
    }
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data
    assert response.data['name'][0] == 'This field may not be blank.'
