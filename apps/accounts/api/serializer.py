from apps.accounts.models import Address
from apps.product.models import Product
from apps.order.models import Order, OrderItem
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name']


class AddressSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    class Meta:
        model = Address
        fields = ['id', 'country', 'province', 'city', 'street', 'pelak', 'complete_address']
