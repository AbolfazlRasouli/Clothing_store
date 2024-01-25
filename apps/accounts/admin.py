from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Address, CustomUser
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group


@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    model = CustomUser
    # inlines = (StaffInline,)
    ordering = ("email",)
    search_fields = ("email", "last_name", "phone")
    list_display = ("email", "phone_number", "first_name", "last_name", "is_staff", "edit", "delete")
    list_display_links = None
    readonly_fields = ("last_login", "date_joined")

    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات یکتا ', {'fields': ('phone_number', 'birthday', 'profile_image', 'user_type', 'is_deleted')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات یکتا ', {'fields': ('phone_number', 'email', 'birthday', 'profile_image', 'user_type', 'is_active', 'is_deleted')}),
    )

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     if obj.user_type == 'e' and obj.is_active:
    #         group, created = Group.objects.get_or_create(name="supervisor")
    #         obj.groups.add(group)
    #         obj.save()
    #         print(obj.groups.all())

    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ("email", "phone_number", "first_name", "last_name", "is_staff", 'show')

    def edit(self, obj):
        url = reverse('admin:accounts_customuser_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:accounts_customuser_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def show(self, obj):
        url = reverse('admin:product_category_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">مشاهده</a>', url)

    show.short_description = 'مشاهده'
    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'pelak', 'edit', 'delete')
    search_fields = ('user__email', 'city', 'street', 'pelak')
    list_filter = ('user', 'city', 'province')
    list_display_links = None

    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ('user', 'city', 'street', 'pelak', 'show')


    def edit(self, obj):
        url = reverse('admin:accounts_address_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self, obj):
        url = reverse('admin:accounts_address_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    def show(self, obj):
        url = reverse('admin:product_category_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">مشاهده</a>', url)

    show.short_description = 'مشاهده'
    edit.short_description = 'ویرایش'
    delete.short_description = 'حذف'



# celery -A src beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler