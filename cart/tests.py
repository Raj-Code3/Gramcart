from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Category
from decimal import Decimal


class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Audio', slug='audio')
        self.product = Product.objects.create(
            name='Sony WH-1000XM5',
            sku='SONY-XM5',
            category=self.category,
            short_description='Headphones',
            description='Noise cancelling headphones.',
            price=Decimal('350.00'),
            stock=10
        )

    def test_cart_add_and_view(self):
        # Add item to cart
        response = self.client.post(
            reverse('cart:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 2}
        )
        self.assertEqual(response.status_code, 302)

        # Check cart page
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sony WH-1000XM5')
        self.assertContains(response, '₹700.00')

    def test_cart_remove(self):
        self.client.post(reverse('cart:cart_add', kwargs={'product_id': self.product.id}), {'quantity': 1})
        response = self.client.get(reverse('cart:cart_remove', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response, 'Your Shopping Bag is empty')

