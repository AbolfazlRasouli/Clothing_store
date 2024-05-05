from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from .models import Order, OrderItem
from apps.product.models import Variant
import json
from django.http import JsonResponse



def cart_view(request):

    if request.method == 'POST':
        received_data = json.loads(request.body)

        print('aaaaaaaaaaaaaa')
        print(received_data)
        product_ids = list(received_data.keys())
        print(product_ids)

        variants_quantity = {}
        for product_id in product_ids:
            product_data = received_data[product_id]
            print(product_id)
            size = product_data['size']
            print(size)
            color = product_data['color']
            print(color)


            variant = Variant.objects.get(product_id=product_id, size__name=size, color__code=color)
            print(variant)
            if variant:
                variants_quantity[product_id] = variant.quantity
            else:
                variants_quantity[product_id] = 0

        print('Variants Quantity:', variants_quantity)

        for product_id, quantity in variants_quantity.items():
            received_data[product_id]['count'] = quantity
        print(received_data)
        request.session['received_data'] = received_data
        return JsonResponse({'message': 'Data processed successfully'})

    else:
        received_data = request.session.get('received_data')
        # print('aaaaaaaaaaaaaa')
        # print(received_data)
        # product_ids = list(received_data.keys())
        # print(product_ids)
        #
        # variants_quantity = {}
        # for product_id in product_ids:
        #     product_data = received_data[product_id]
        #     print(product_id)
        #     size = product_data['size']
        #     print(size)
        #     color = product_data['color']
        #     print(color)
        #
        #     variant = Variant.objects.get(product_id=product_id, size__name=size, color__code=color)
        #     print(variant)
        #     if variant:
        #         variants_quantity[product_id] = variant.quantity
        #     else:
        #         variants_quantity[product_id] = 0
        #
        # print('Variants Quantity:', variants_quantity)
        #
        # for product_id, quantity in variants_quantity.items():
        #     received_data[product_id]['quantity'] = quantity
        # print(received_data)


        return render(request, 'order/cart.html',{'received_data': received_data})


def show_buy(request):
    return render(request, 'order/showbuy.html')












 # variant = Variant.objects.filter(product_id=product_id, size__name=size, color__code=color)
