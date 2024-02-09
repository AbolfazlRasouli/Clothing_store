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
