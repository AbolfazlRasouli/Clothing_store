from django.contrib import admin

from .models import Address, CustomUser

admin.site.register([CustomUser, Address])
