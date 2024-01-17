from django.contrib import admin

from .models import Product, Attribute, Comment, Category, Image, Discount, Like

admin.site.register([Product, Attribute, Comment, Category, Image, Discount, Like])
