from django.shortcuts import render


def home(request):
    return render(request, 'product/home_product.html')
