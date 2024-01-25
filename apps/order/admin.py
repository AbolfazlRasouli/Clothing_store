from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ("status", "user", "address", "edit", "delete",)
    # readonly_fields = ("user",)
    search_fields = ("user",)
    list_display_links = None

    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ("status", "user", "address",'show')

    def edit(self, obj):
        url = reverse('admin:order_order_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:order_order_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def show(self, obj):
        url = reverse('admin:order_order_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">مشاهده</a>', url)

    show.short_description = 'مشاهده'
    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ("product", "order", "size", "color", "price", "count", "edit", "delete",)
    # readonly_fields = ("user",)
    search_fields = ("product", "order", "size", "color", "price",)
    list_display_links = None

    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ("product", "order", "size", "color", "price", "count", 'show')

    def edit(self, obj):
        url = reverse('admin:order_orderitem_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:order_orderitem_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def show(self, obj):
        url = reverse('admin:order_orderitem_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">مشاهده</a>', url)

    show.short_description = 'مشاهده'
    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'
