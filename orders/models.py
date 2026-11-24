import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('ordered', 'Order Placed'),
        ('processing', 'Processing & Packing'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Payment Received'),
        ('failed', 'Payment Failed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit / Debit Card'),
        ('paypal', 'UPI (Google Pay, PhonePe, Paytm)'),
        ('cod', 'Cash on Delivery (COD)'),
        ('applepay', 'Net Banking / Wallets'),
    ]

    DELIVERY_METHOD_CHOICES = [
        ('standard', 'Standard Delivery (3-7 Business Days)'),
        ('express', 'Express Delivery (1-2 Business Days)'),
        ('same_day', 'Same-Day Priority Delivery'),
    ]

    order_number = models.CharField(max_length=64, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Customer details
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    
    # Shipping Address snapshot
    shipping_address = models.CharField(max_length=255)
    apartment_suite = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    
    # Delivery & Payment
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHOD_CHOICES, default='standard')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='paid')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='ordered')
    
    # Financial breakdown
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Logistics
    tracking_number = models.CharField(max_length=60, blank=True, null=True)
    carrier = models.CharField(max_length=60, default='GramKart Express')
    estimated_delivery = models.DateField(null=True, blank=True)
    delivery_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            today_str = datetime.date.today().strftime('%Y%m%d')
            random_part = uuid.uuid4().hex[:6].upper()
            self.order_number = f"ORD-{today_str}-{random_part}"
        if not self.tracking_number:
            self.tracking_number = f"TRK-{uuid.uuid4().hex[:8].upper()}"
        if not self.estimated_delivery:
            days = 4 if self.delivery_method == 'standard' else (2 if self.delivery_method == 'express' else 1)
            self.estimated_delivery = datetime.date.today() + datetime.timedelta(days=days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number} - {self.full_name}"

    @property
    def progress_percentage(self):
        status_map = {
            'ordered': 20,
            'processing': 45,
            'shipped': 70,
            'out_for_delivery': 90,
            'delivered': 100,
            'cancelled': 0,
        }
        return status_map.get(self.order_status, 10)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
    product_name = models.CharField(max_length=255)
    product_image_url = models.URLField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in {self.order.order_number}"

    @property
    def total_price(self):
        return self.price * self.quantity

