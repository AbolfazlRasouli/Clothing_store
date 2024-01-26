from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, TemplateView, CreateView
from django.db.models import Q, F
from .models import Product, Attribute, Discount, Category, Image, Comment, Like
from .forms import CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class HomePage(ListView):
    model = Product
    template_name = 'product/home_product.html'
    context_object_name = 'products'
    # paginate_by = 1
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
        product = self.get_object()
        comments = Comment.objects.filter(product=product, status=Comment.COMMENT_STATUS_APPROVED)
        # context['comments'] = comments
        # context['images'] = self.object.images.all()
        # context['attributes'] = self.object.attribute.all()
        context['comments'] = comments
        context['images'] = product.images.all()
        context['attributes'] = product.attribute.all()
        context['comment_form'] = CommentForm()

        # print(self.object)
        # print(self.object.price)
        # print(context['images'])
        # print(context['attributes'])
        return context


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



# def item_search(request):
#     search_query = request.GET.get('search')
#     search = Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(category__name__icontains=search_query))
#     return render(request, 'cafemenu/search.html', {'searchs': search})
