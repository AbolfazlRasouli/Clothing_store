from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, TemplateView
from django.db.models import Q, F
from .models import Product, Attribute, Discount, Category, Image, Comment, Like


class HomePage(ListView):
    model = Product
    template_name = 'product/home_product.html'
    context_object_name = 'products'
    queryset = Product.objects.prefetch_related('images')
    print(queryset)


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'product/category_product.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        print(category, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        subcategory = Category.objects.filter(replay_cat=category)
        print(subcategory,'bbbbbbbbbbbbbbbbbbbbbbbbbbbb')
        if subcategory.exists():
            products = Product.objects.filter(category__in=subcategory)
            # context['subcategory'] = subcategory
            print(products, 'cccccccccccccccccccccccccccccccccccccccccc')
        else:
            products = Product.objects.filter(category=category)
            print(products, 'dddddddddddddddddddddddddddddddddddddddddddd')
        context['products'] = products
        print(context, 'e' * 100)
        return context




class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail_product.html'
    context_object_name = 'details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # description_lines = self.object.description.splitlines()
        # context['description_lines'] = description_lines


        # context['images'] = Product.objects.select_related('image')
        # context['attributs'] = Product.objects.prefetch_related('attribute')


        context['images'] = self.object.images.all()
        context['attributes'] = self.object.attribute.all()
        print(self.object)
        print((self.object.price))
        print(context['images'])
        print(context['attributes'])
        return context


# def home(request):
#     return render(request, 'product/home_product.html')


# def category(request):
#     return render(request, 'product/category_product.html')

# def detail(request,slug):
#     return render(request, 'product/detail_product.html')
