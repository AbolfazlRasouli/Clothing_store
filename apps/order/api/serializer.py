from apps.accounts.models import Address
from apps.product.models import Product, Variant, Size, Color
from apps.order.models import Order, OrderItem
from django.contrib.auth import get_user_model
from rest_framework import serializers


# class SizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Size
#         fields = ['name',]
#
#
# class ColorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Color
#         fields = ['code',]
#
#
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id',]
#
#
# class VariantSerializer(serializers.ModelSerializer):
#     size = SizeSerializer()
#     color = ColorSerializer()
#     product = ProductSerializer()
#
#     class Meta:
#         model = Variant
#         fields = ['id', 'product', 'size', 'color', 'quantity']


class OrderCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'user', 'address']


class OrderItemCartSerializer(serializers.ModelSerializer):

    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['size', 'color', 'count', 'price', 'order', 'product']

# class ProductSerializer(serializers.ModelSerializer):
#     attributes = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Product
#         fields = ['id', 'attributes']
#
#     def get_attributes(self, obj):
#
#         attributes = obj.attribute.all()
#         attributes_list = []
#         for attribute in attributes:
#             attribute_data = {
#                 'size': attribute.size,
#                 'code_color': attribute.code_color,
#                 'count': attribute.count,
#             }
#             attributes_list.append(attribute_data)
#
#         return attributes_list


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
