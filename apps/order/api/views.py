from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import redirect, reverse
from django.shortcuts import get_object_or_404
from apps.product.models import Product, Variant
from apps.order.models import Order, OrderItem
from .serializer import OrderItemSerializer, OrderItemCartSerializer, OrderCartSerializer
from django.db.models import F
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


class CartAPI(APIView):
    def post(self, request):

        # cart = request.data
        # print('kol dict : ', cart)

        cart_data = request.data.get('cart', {})
        address_id = request.data.get('addressId')

        # print('cart : ', cart_data)
        # print('address_id : ', address_id)
        # product_ids = cart_data.keys()
        # print('idsss products : ', product_ids)

        for item_id, item_data in cart_data.items():
            size = item_data.get('size')
            color = item_data.get('color')
            quantity = item_data.get('quantity')
            try:
                variant = Variant.objects.get(product_id=item_id, size__name=size, color__code=color)
                print('vaiant : ', variant)
                if int(item_data['quantity']) > variant.quantity:
                    print('no')
                    return Response({'error': f'موجودی محصول با شناسه {item_id} کافی نیست.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                # print('oooooooooooooooooooooooooooooooooooooooooooookkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            except ObjectDoesNotExist:
                # print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
                return Response({'error': 'محصول مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)
            print('ok')

        order_serializer = OrderCartSerializer(
            data={'status': Order.ORDER_STATUS_PAID, 'user': request.user.id, 'address': address_id})
        print('oreder1')

        order_serializer.is_valid(raise_exception=True)
        print('oreder2')
        order = order_serializer.save()
        print('oreder3')


        for item_id, item_data in cart_data.items():
            product_id = item_id
            size = item_data.get('size')
            color = item_data.get('color')
            quantity = item_data.get('quantity')
            print('variant1')

            try:
                variant = Variant.objects.get(product_id=product_id, size__name=size, color__code=color)
                product = get_object_or_404(Product, pk=item_id)
                print('variant3')
            except Variant.DoesNotExist:
                print('variant4')
                return Response({'error': f'محصول با شناسه {product_id} یا ویژگی‌های مورد نظر یافت نشد.'},
                                status=status.HTTP_404_NOT_FOUND)

            print('variant5')
            order_item_serializer = OrderItemCartSerializer(
                data={'size': size, 'color': color, 'count': quantity, 'price': product.calculate_discounted_price(),
                      'order': order.id, 'product': product.id})
            order_item_serializer.is_valid(raise_exception=True)
            order_item_serializer.save()
            print('variant6')

            Variant.objects.filter(id=variant.pk).update(quantity=F('quantity') - int(quantity))
            print('variant7')

        return Response({'success': 'سفارش با موفقیت ثبت شد.'}, status=status.HTTP_201_CREATED)


        # for item_id, item_data in cart_data.items():
        #     size = item_data.get('size')
        #     color = item_data.get('color')
        #     quantity = item_data.get('quantity')
        #
        #
        #     product_data = {
        #         'id': item_id,
        #         'size': size,
        #         'color': color,
        #         'quantity': quantity,
        #     }
        #
        #     serializer = ProductSerializer(data=product_data)
        #
        #     if serializer.is_valid():
        #         order = Order.objects.create(status=Order.ORDER_STATUS_PAID, user=request.user)
        #
        #         product = get_object_or_404(Product, pk=item_id)
        #         print(serializer)
        #         order_item = OrderItem.objects.create(
        #             size=size,
        #             color=color,
        #             count=quantity,
        #             price=product.calculate_discounted_price(),
        #             order=order,
        #             product=product
        #         )
        #         print('okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        #         print('product : ', product)
        #         print('size : ', size)
        #         print('color : ', color)
        #
        #         attribute = product.attribute.filter(size=size, name_color=color)
        #         print(attribute)
        #         if attribute:
        #             attribute.count = F('count') - quantity
        #             attribute.save()
        #
        #
        #
        #     else:
        #
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #
        # return Response({"message": "Data received successfully"})


class ShowCartApi(APIView):
    def get(self, request):
        order_item_queryser = OrderItem.objects.filter(order__user=request.user)
        serializer = OrderItemSerializer(order_item_queryser, many=True)
        return Response(serializer.data)
