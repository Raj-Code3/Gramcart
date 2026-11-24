from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import Category, Brand, Product, Review, Wishlist


class ProductCatalogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.brand = Brand.objects.create(name='Apple', slug='apple')
        self.product = Product.objects.create(
            name='MacBook Air M2',
            sku='MBA-M2-001',
            category=self.category,
            brand=self.brand,
            short_description='Thin and light laptop',
            description='Detailed MacBook description with Apple silicon.',
            price=Decimal('1199.00'),
            discount_price=Decimal('999.00'),
            stock=15
        )
        self.user = User.objects.create_user(username='testbuyer', password='buyerpassword123')

    def test_product_list_view(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MacBook Air M2')
        self.assertContains(response, '₹999.00')

    def test_product_search_and_filter(self):
        # Keyword search
        response = self.client.get(reverse('products:product_list'), {'q': 'MacBook'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MacBook Air M2')

        # Category filter
        response = self.client.get(reverse('products:product_list'), {'category': 'electronics'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MacBook Air M2')

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MacBook Air M2')
        self.assertContains(response, 'MBA-M2-001')

    def test_add_review(self):
        self.client.login(username='testbuyer', password='buyerpassword123')
        response = self.client.post(
            reverse('products:add_review', kwargs={'slug': self.product.slug}),
            {'rating': 5, 'headline': 'Super fast!', 'comment': 'Love the battery life.'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.product.reviews.count(), 1)
        self.assertEqual(self.product.average_rating, 5.0)

    def test_wishlist_toggle(self):
        self.client.login(username='testbuyer', password='buyerpassword123')
        # Add to wishlist
        response = self.client.get(
            reverse('products:toggle_wishlist', kwargs={'product_id': self.product.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Wishlist.objects.filter(user=self.user, product=self.product).exists())

