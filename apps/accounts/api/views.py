from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, reverse
from django.shortcuts import get_object_or_404
from apps.product.models import Product
from apps.order.models import Order, OrderItem
from .serializer import UserSerializer


class ProfileAPI(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        print(request.data)
        print('sssssssssssssssssssssssssssssssssssss')
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



