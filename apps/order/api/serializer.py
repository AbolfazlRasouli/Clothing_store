from apps.accounts.models import Address
from apps.product.models import Product
from apps.order.models import Order, OrderItem
from django.contrib.auth import get_user_model
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'attributes']

    def get_attributes(self, obj):

        attributes = obj.attribute.all()
        attributes_list = []
        for attribute in attributes:
            attribute_data = {
                'size': attribute.size,
                'code_color': attribute.code_color,
                'count': attribute.count,
            }
            attributes_list.append(attribute_data)

        return attributes_list


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'create_at']


class ProductCartShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image']


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductCartShowSerializer()

    class Meta:
        model = OrderItem
        fields = ['size', 'color', 'count', 'price', 'order', 'product']
