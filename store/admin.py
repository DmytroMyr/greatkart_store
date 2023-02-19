from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = { 'slug': ('title',) }
