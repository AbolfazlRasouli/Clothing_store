from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html
from .models import Product, Attribute, Comment, Category, Image, Discount, Like
from django.urls import reverse
from .mixin import CustomAdminMixin


class ProductInline(admin.StackedInline):
    model = Product
    extra = 0
    classes = ('collapse',)
    fieldsets = (
        (None, {'fields': ('name', 'code', 'price')}),
    )


class CommenApprovedInline(admin.StackedInline):
    model = Comment
    verbose_name = "نظر"
    classes = ('collapse',)
    readonly_fields = ("user",)
    fieldsets = (
        (None, {"fields": ("body", "product", "user")}),
    )
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status="a")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ("name", "display_image", "edit", "delete",)
    readonly_fields = ("display_image",)
    search_fields = ("name",)
    list_display_links = None
    inlines = (ProductInline,)

    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ('name', 'display_image', 'show')

    def display_image(self, obj):
        return format_html('<img src="{}" height="60" style="background-color: #121212;"/>'.format(obj.image.url))

    def edit(self, obj):
        url = reverse('admin:product_category_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:product_category_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def show(self, obj):
        url = reverse('admin:product_category_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">مشاهده</a>', url)

    display_image.short_description = "تصویر موجود"
    show.short_description = 'مشاهده'
    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    list_display = ('size', 'name_color', 'display_code_color', 'count', 'edit', 'delete')
    search_fields = ('size', 'name_color', 'code_color')
    list_filter = ('size', 'name_color', 'count')
    list_display_links = None

    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ('size', 'name_color', 'display_code_color', 'count', 'show')

    def edit(self, obj):
        url = reverse('admin:product_attribute_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:product_attribute_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def display_code_color(self, obj):
        return format_html('<div style="width: 40px; height: 40px; background-color: {};"></div>', obj.code_color)

    def show(self, obj):
        url = reverse('admin:product_attribute_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">مشاهده</a>', url)

    display_code_color.short_description = 'رنگ'
    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'
    show.short_description = 'مشاهده'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    model = Discount
    list_display = ('name', 'code', 'start_date', 'end_date', 'count', 'edit', 'delete')
    search_fields = ('name', 'code')
    list_filter = ('name', 'code', 'count')
    list_display_links = None

    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ('name', 'code', 'start_date', 'end_date', 'count', 'show')

    def edit(self, obj):
        url = reverse('admin:product_discount_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:product_discount_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def show(self, obj):
        url = reverse('admin:product_discount_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">مشاهده</a>', url)

    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'
    show.short_description = 'مشاهده'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'code', 'price', 'display_image', 'edit', 'delete')
    search_fields = ('name', 'category__name')
    list_filter = ('name', 'category__name')
    list_display_links = None
    inlines = (CommenApprovedInline,)

    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ('name', 'code', 'price', 'display_image', 'show')



    # def get_list_display(self, request):
    #     if request.user.is_superuser:
    #         return super().get_list_display(request)
    #     elif request.user.groups.filter(name='supervisor').exists():
    #             return ('name', 'code', 'price', 'display_image', 'show')


    def edit(self, obj):
        url = reverse('admin:product_product_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:product_product_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def display_image(self, obj):
        return format_html('<img src="{}" height="60" style="background-color: #121212;"/>'.format(obj.image.url))

    def show(self, obj):
        url = reverse('admin:product_product_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">مشاهده</a>', url)

    display_image.short_description = "تصویر موجود"
    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'
    show.short_description = 'مشاهده'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ("display_image", "edit", "delete",)
    readonly_fields = ("display_image",)
    search_fields = ("product__name",)
    list_display_links = None

    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ('display_image', 'show')

    def display_image(self, obj):
        return format_html('<img src="{}" height="60" style="background-color: #121212;"/>'.format(obj.image.url))

    def edit(self, obj):
        url = reverse('admin:product_image_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:product_image_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def show(self, obj):
        url = reverse('admin:product_image_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">مشاهده</a>', url)

    display_image.short_description = "تصویر موجود"
    show.short_description = 'مشاهده'
    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', "edit", "delete")
    search_fields = ('product__name', 'user__username',)
    # list_filter = ('created_at',)
    # readonly_fields = ('created_at', 'updated_at',)
    list_display_links = None

    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ('product', 'user', 'show')

    def edit(self, obj):
        url = reverse('admin:product_like_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:product_like_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def show(self, obj):
        url = reverse('admin:product_like_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">مشاهده</a>', url)

    show.short_description = 'مشاهده'
    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ("product", "user", "status", "edit", "delete",)
    search_fields = ("product", "user",)
    list_display_links = None
    # inlines = (ProductInline,)

    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ("product", "user", "status", 'show')

    def edit(self, obj):
        url = reverse('admin:product_comment_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:product_comment_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def show(self, obj):
        url = reverse('admin:product_comment_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">مشاهده</a>', url)

    show.short_description = 'مشاهده'
    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'




