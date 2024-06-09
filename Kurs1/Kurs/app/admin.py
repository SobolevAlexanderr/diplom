from django.contrib import admin
from .models import ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(ProductImage)