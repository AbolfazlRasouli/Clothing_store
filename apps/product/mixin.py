
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.options import ModelAdmin
from .models import Product


class CustomAdminMixin(ModelAdmin):
    def get_list_display(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'operator' in user_groups:
            return super().get_list_display(request)
        elif 'manager' in user_groups:
            return super().get_list_display(request)
        else:
            return ('show',)