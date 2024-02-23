from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, reverse
from django.shortcuts import get_object_or_404
from apps.product.models import Product
from apps.order.models import Order, OrderItem
from .serializer import ProductSerializer, OrderItemSerializer
from django.db.models import F

class CartAPI(APIView):
    def post(self, request):
        cart_data = request.data

        for item_id, item_data in cart_data.items():
            size = item_data.get('size')
            color = item_data.get('color')
            quantity = item_data.get('quantity')


            product_data = {
                'id': item_id,
                'size': size,
                'color': color,
                'count': quantity,
            }

            serializer = ProductSerializer(data=product_data)

            if serializer.is_valid():
                order = Order.objects.create(status=Order.ORDER_STATUS_PAID, user=request.user)

                product = get_object_or_404(Product, pk=item_id)
                print(serializer)
                order_item = OrderItem.objects.create(
                    size=size,
                    color=color,
                    count=quantity,
                    price=product.calculate_discounted_price(),
                    order=order,
                    product=product
                )
                print('okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
                print('product : ', product)
                print('size : ', size)
                print('color : ', color)

                attribute = product.attribute.filter(size=size, name_color=color)
                print(attribute)
                if attribute:
                    attribute.count = F('count') - quantity
                    attribute.save()



            else:

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Data received successfully"})



class ShowCartApi(APIView):
    def get(self, request):

        order_item_queryser = OrderItem.objects.filter(order__user=request.user)
        serializer = OrderItemSerializer(order_item_queryser, many=True)
        return Response(serializer.data)
