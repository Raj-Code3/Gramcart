from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Product, Category
from orders.models import Order
from decimal import Decimal


class OrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='johndoe', password='password123', email='john@example.com')
        self.category = Category.objects.create(name='Computers', slug='computers')
        self.product = Product.objects.create(
            name='Dell XPS 15',
            sku='DELL-XPS15',
            category=self.category,
            short_description='Performance laptop',
            description='Intel Core i9 laptop.',
            price=Decimal('2000.00'),
            stock=5
        )

    def test_checkout_and_order_creation(self):
        # 1. Add product to cart
        self.client.post(reverse('cart:cart_add', kwargs={'product_id': self.product.id}), {'quantity': 1})
        
        # 2. Login user
        self.client.login(username='johndoe', password='password123')

        # 3. Post Checkout Form
        checkout_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '+91 98765 11222',
            'shipping_address': '123 Main Street',
            'apartment_suite': 'Suite 100',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'postal_code': '400001',
            'country': 'India',
            'delivery_method': 'express',
            'payment_method': 'card',
            'card_number': '4242424242424242',
            'card_expiry': '12/28',
            'card_cvv': '123',
            'save_address': True
        }

        response = self.client.post(reverse('orders:checkout'), checkout_data)
        self.assertEqual(response.status_code, 302)

        # 4. Verify order created
        order = Order.objects.filter(email='john@example.com').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.shipping_fee, Decimal('149.00')) # Express shipping
        
        # 5. Check product inventory decreased from 5 to 4
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 4)

        # 6. Test order detail view
        detail_res = self.client.get(reverse('orders:order_detail', kwargs={'order_number': order.order_number}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertContains(detail_res, 'Dell XPS 15')

