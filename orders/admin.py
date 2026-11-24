from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity', 'total_price')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'grand_total', 'payment_status', 'order_status', 'created_at', 'delivery_method')
    list_filter = ('order_status', 'payment_status', 'delivery_method', 'created_at')
    list_editable = ('order_status', 'payment_status')
    search_fields = ('order_number', 'full_name', 'email', 'phone_number', 'tracking_number')
    readonly_fields = ('order_number', 'tracking_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Identification', {
            'fields': ('order_number', 'user', 'tracking_number', 'created_at', 'updated_at')
        }),
        ('Customer & Delivery Details', {
            'fields': ('full_name', 'email', 'phone_number', 'shipping_address', 'apartment_suite', 'city', 'state', 'postal_code', 'country', 'delivery_instructions')
        }),
        ('Logistics & Fulfillment', {
            'fields': ('delivery_method', 'order_status', 'carrier', 'estimated_delivery')
        }),
        ('Financial Summary', {
            'fields': ('payment_method', 'payment_status', 'subtotal', 'shipping_fee', 'tax_amount', 'discount_amount', 'grand_total')
        }),
    )

