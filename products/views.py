from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderListSerializer,NewProductSerializer,AddStockSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product



class ProductsView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'products': openapi.Schema(
                    type=openapi.TYPE_OBJECT,  
                        properties={
                            'sku': openapi.Schema(type=openapi.TYPE_STRING, description='SKU of the product'),
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the product'),
                        },
                        example={
                            "sku": "1",
                            "quantity": 10
                        },
                    description='New product data'
                )
            },
            example={  
                        "sku": "31",
                        "name": "jabon colorido" 
                
            }
        ),
        responses={
            200: openapi.Response('Success', NewProductSerializer),
            400: 'Bad Request'
        },
        operation_description="Verificar que el sku no exista previamente,se crea un nuevo producto segun el sku indicado(por default su stock es 100)",
        operation_summary="Creacion de un nuevo producto"
    )
    def post(self, request, *args, **kwargs):
        serializer = NewProductSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
 
            sku = validated_data['sku']
            name = validated_data['name'] 
            # print(sku,name)
            Product.objects.create(sku=sku,name=name)

            return Response({"message": "Product created"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class InventoriesView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'products': openapi.Schema(
                    type=openapi.TYPE_OBJECT,  
                        properties={
                            'amount': openapi.Schema(type=openapi.TYPE_INTEGER, description='New amount to add at the product stock'), 
                        },
                        example={ 
                            "amount": 10
                        },
                    description='New product stock'
                )
            },
            example={  
                        "amount": 10 
            }
        ),
        responses={
            200: openapi.Response('Success', OrderListSerializer),
            400: 'Bad Request'
        },
        operation_description="Se incrementa el stock en la cantidad indicada del producto dado, verificar que el sku sea valido",
        operation_summary="Actualizacion del stock de un producto"
    )
    def patch(self, request, *args, **kwargs): 
        product_id = kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AddStockSerializer(data=request.data )

        if serializer.is_valid():
            validated_data = serializer.validated_data 
            additional_stock = validated_data['amount']
            product.stock += additional_stock
            product.save()
            
            return Response({"message": "Order received"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class OrderListView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'products': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'sku': openapi.Schema(type=openapi.TYPE_STRING, description='SKU of the product'),
                            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity of the product'),
                        },
                        example={
                            "sku": "1",
                            "quantity": 10
                        }
                    ),
                    description='List of products'
                )
            },
            example={
                "products": [
                    {
                        "sku": "1",
                        "quantity": 10
                    },
                    {
                        "sku": "2",
                        "quantity": 20
                    }
                ]
            }
        ),
        responses={
            200: openapi.Response('Success', OrderListSerializer),
            400: 'Bad Request'
        },
        operation_description="""Disminuye el inventario segun la cantidad indicada en el 
        producto a comprar, si el monto de stock de un producto es inferior a la cantidad solicitada
        no se permite la transaccion, verificar que el sku sea valido""",
        operation_summary="Ejecucion de una orden de compra"
    )
    def post(self, request, *args, **kwargs):
        serializer = OrderListSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            for product_data in validated_data['products']:
                sku = product_data['sku']
                quantity = product_data['quantity']
                
                product_instance = Product.objects.get(sku=sku)
                product_instance.stock = product_instance.stock - int(quantity)
                product_instance.save()
            return Response({"message": "Order received"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


