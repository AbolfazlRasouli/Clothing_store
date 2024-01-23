from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, TemplateView
from django.db.models import Q, F


class HomePage(ListView):
    pass


class CategoryView(ListView):
    pass


class CategoryDetailView(ListView):
    pass


class ItemsView(ListView):
    pass


class ItemsDetailView(DetailView):
    pass


def home(request):
    return render(request, 'product/home_product.html')


def category(request):
    return render(request, 'product/category_product.html')

def detail(request,slug):
    return render(request, 'product/detail_product.html')
