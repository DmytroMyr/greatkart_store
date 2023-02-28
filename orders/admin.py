from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'variation','quantity', 'product_price', 'ordered')
    extra = 0


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'product_price', 'ordered', 'created_at')
    list_filter = ('ordered', 'created_at')
    search_fields = ('order__order_number', 'product__title')
    readonly_fields = ('payment', 'user', 'product', 'product_price', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('order', 'payment', 'user', 'product', 'variation')
        }),
        ('Details', {
            'fields': ('quantity', 'product_price', 'ordered')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display = ('order_number', 'full_name', 'email', 'phone', 'order_total', 'status', 'is_ordered', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__email', 'user__username', 'first_name', 'last_name', 'email', 'phone', 'city', 'address')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('user', 'payment', 'order_number', 'status', 'ip', 'is_ordered')
        }),
        ('Billing Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'city', 'address', 'tax', 'order_total')
        }),
        ('Additional Info', {
            'fields': ('comment',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        # Disable adding new orders from the admin site
        return False
    

admin.site.register(Payment)
