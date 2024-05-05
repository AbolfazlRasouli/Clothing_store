from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, TemplateView, CreateView
from django.views import View
from django.db.models import Q, F
from .models import Product, Discount, Category, Image, Comment, Like, Variant
from .forms import CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt


class HomePage(ListView):
    model = Product
    # model = Variant
    template_name = 'product/home_product.html'
    context_object_name = 'products'
    paginate_by = 2
    # queryset = Variant.objects.select_related('product', 'discount').distinct()
    queryset = Product.objects.prefetch_related('images', 'variant_product')
    print(queryset)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_products'] = Product.objects.prefetch_related('images').order_by('-create_at')[:10]
        return context


# class CategoryDetailView(DetailView):
#     model = Category
#     template_name = 'product/category_product.html'
#     paginate_by = 2
#     context_object_name = 'categories'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category = self.get_object()
#         print(category, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#         subcategory = Category.objects.filter(replay_cat=category)
#         print(subcategory,'bbbbbbbbbbbbbbbbbbbbbbbbbbbb')
#         if subcategory.exists():
#             products = Product.objects.filter(category__in=subcategory)
#             # context['subcategory'] = subcategory
#             print(products, 'cccccccccccccccccccccccccccccccccccccccccc')
#         else:
#             products = Product.objects.filter(category=category)
#             print(products, 'dddddddddddddddddddddddddddddddddddddddddddd')
#         context['products'] = products
#         print(context, 'e' * 100)
#         return context


class CategoryProductListView(ListView):

    template_name = 'product/category_product.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        pass
        cat = Category.objects.get(pk=self.kwargs['pk'])
        subcategories = Category.objects.filter(replay_cat=cat)
        if subcategories.exists():
            queryset = Product.objects.filter(category__in=subcategories)
        else:
            queryset = Product.objects.filter(category=cat)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = Category.objects.get(pk=self.kwargs['pk'])
        return context


class ProductDetailView(DetailView):
    # pass
    model = Product
    template_name = 'product/detail_product.html'
    context_object_name = 'details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        comments = Comment.objects.filter(product=product, status=Comment.COMMENT_STATUS_APPROVED)
        context['comments'] = comments
        context['images'] = product.images.all()
        context['comment_form'] = CommentForm()
        variants = Variant.objects.filter(product=product)
        print(variants)


        size = []
        size_color_dict = {}
        count = {}

        for variant in variants:
            size.append(variant.size)
        size = list(set(size))
        print(size)


        for variant in variants:
            # if variant.size not in size_color_dict:
                # size_color_dict[variant.size] = [variant.color]
            a = size_color_dict.setdefault(variant.size.name, [])
            a.append(variant.color.code)
            # else:
            #     # a = size_color_dict[variant.size].append(variant.color)
            #     a= size_color_dict.setdefault(variant.size.name, [variants.color])

        # for variant in variants:
        #     a = count.setdefault(variant.size.name, [])
        #     a.append(variant.quantity)

        print(size_color_dict)
        context['sizes'] = size
        context['colors'] = size_color_dict
        return context
        # context['attributes'] = self.object.attribute.all()
        # context['comments'] = comments
        # context['images'] = self.object.images.all()
        # context['attributes'] = product.attribute.all()
        # context['sizes'] = product.attribute.values_list('size', flat=True).distinct()
        # context['colors'] = product.attribute.values_list('code_color', flat=True).distinct()
        # print(self.object)
        # print(self.object.price)
        # print(context['images'])
        # print(context['attributes'])


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('product:home_page')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user

        product_id = int(self.kwargs['details_id'])
        product = get_object_or_404(Product, id=product_id)
        obj.product = product
        return super().form_valid(form)


def item_search(request):
    search_query = request.GET.get('search')
    search = Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(category__name__icontains=search_query))
    return render(request, 'product/category_product.html', {'products': search})


class LikeProductView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        user = request.user
        if Like.objects.filter(product_id=product_id, user=user).exists():
            return JsonResponse({'error': _('You have already liked this product.')}, status=400)

        Like.objects.create(product_id=product_id, user=user)
        return JsonResponse({'message': _('product liked')})
