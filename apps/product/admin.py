from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html
from .models import Product, Attribute, Comment, Category, Image, Discount, Like
from django.urls import reverse

admin.site.register([Comment, Image, Like])


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ("name", "display_image", "edit", "delete")
    readonly_fields = ("display_image",)
    search_fields = ("name",)
    list_display_links = None

    def display_image(self, obj):
        return format_html('<img src="{}" height="60" style="background-color: #121212;"/>'.format(obj.image.url))

    display_image.short_description = "تصویر موجود"

    def edit(self, obj):
        url = reverse('admin:product_category_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:product_category_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    list_display = ('size', 'name_color', 'display_code_color', 'count', 'edit', 'delete')
    search_fields = ('size', 'name_color', 'code_color')
    list_filter = ('size', 'name_color', 'count')
    list_display_links = None

    def edit(self, obj):
        url = reverse('admin:product_attribute_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:product_attribute_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def display_code_color(self, obj):
        return format_html('<div style="width: 40px; height: 40px; background-color: {};"></div>', obj.code_color)

    display_code_color.short_description = 'رنگ'

    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    model = Discount
    list_display = ('name', 'code', 'start_date', 'end_date', 'count', 'edit', 'delete')
    search_fields = ('name', 'code')
    list_filter = ('name', 'code', 'count')
    list_display_links = None

    def edit(self, obj):
        url = reverse('admin:product_discount_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:product_discount_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'


# class AttributeInline(admin.TabularInlin):
#     model = Attribute


class CategoryInline(admin.StackedInline):
    model = Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'code', 'price', 'display_image', 'edit', 'delete')
    search_fields = ('name', 'category__name')
    list_filter = ('name','category__name')
    # inlines = (CategoryInline,)
    list_display_links = None

    def edit(self, obj):
        url = reverse('admin:product_product_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:product_product_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def display_image(self, obj):
        return format_html('<img src="{}" height="60" style="background-color: #121212;"/>'.format(obj.image.url))

    display_image.short_description = "تصویر موجود"

    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'