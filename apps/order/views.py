from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from .models import Order, OrderItem


def cart_view(request):
    return render(request, 'order/cart.html')
