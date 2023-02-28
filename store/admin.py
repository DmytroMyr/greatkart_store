from django.contrib import admin
from .models import Product, Variations, ReviewRating


class VariationsAdmin(admin.TabularInline):
    model = Variations
    raw_id_fields = ['product']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [VariationsAdmin]
    list_display = ('title', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = { 'slug': ('title',) }


@admin.register(Variations)
class AllVariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'category', 'value', 'is_active', 'created_date')
    list_editable = ('is_active',)
    list_filter = ('product', 'category', 'value', 'is_active', 'created_date')


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'review', 'rating', 'status', 'created_at', 'updated_at')
