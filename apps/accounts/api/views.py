from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, reverse
from django.shortcuts import get_object_or_404
from apps.product.models import Product
from apps.order.models import Order, OrderItem
from .serializer import UserSerializer, AddressSerializer
from apps.accounts.models import Address


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



class AddressApi(APIView):
    def get(self, request):
        address_queryser = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(address_queryser, many=True)
        return Response(serializer.data)


class DetailAddress(APIView):
    def get(self, request, pk):
        address_querset = get_object_or_404(Address.objects.select_related('user'), pk=pk)
        serializer = AddressSerializer(address_querset)
        return Response(serializer.data)

    def put(self, request, pk):
        address_instance = get_object_or_404(Address, pk=pk)
        serializer = AddressSerializer(address_instance, data=request.data)
        print('*' * 10)
        print(request.data)
        if serializer.is_valid():
            print('*' * 20)
            serializer.save()
            return Response(serializer.data)
        print('*' * 100)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def put(self, request, pk):
    #     print('*' * 10)
    #     address_queryset = get_object_or_404(Address.objects.filter(user=request.user), pk=pk)
    #     print('*' * 20)
    #     print(request.data)
    #     serializer = AddressSerializer(address_queryset, data=request.data)
    #     print('*' * 30)
    #
    #     if serializer.is_valid():
    #         print('*' * 40)
    #
    #         serializer.save()
    #         print('*' * 50)
    #
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # serializer.is_valid(raise_exception=True)
        # print('*' * 40)
        #
        # serializer.save()
        # print('*' * 50)
        #
        # return Response(serializer.data)

