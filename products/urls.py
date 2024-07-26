from django.urls import path
from .views import OrderListView, ProductsView, InventoriesView

urlpatterns =  [ 
    path("products", ProductsView.as_view(), name="products"),
    path('inventories/product/<int:product_id>', InventoriesView.as_view(), name='inventories_product'),
    path("orders", OrderListView.as_view(), name="orders"),
]