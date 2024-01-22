from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Address, CustomUser
from django.utils.html import format_html
from django.urls import reverse


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
        ('اطلاعات یکتا ', {'fields': ('phone_number', 'birthday', 'profile_image', 'is_deleted')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات یکتا ', {'fields': ('phone_number', 'birthday', 'profile_image', 'is_deleted')}),
    )

    def edit(self, obj):
        url = reverse('admin:accounts_customuser_change', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #00ff40; padding:8px">ویرایش</a>', url)

    def delete(self,obj):
        url = reverse('admin:accounts_customuser_delete', args=[obj.id])
        return format_html('<a href="{}" style="color:white; background-color: #840303; padding:8px">حذف</a>', url)

    edit.short_description = 'ویرایش'
    edit.short_description = 'حذف'

