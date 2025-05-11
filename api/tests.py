from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from restaurant.models import Product, Category, Order, OrderItem


class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

        self.category = Category.objects.create(name='Jedzenie')
        self.product = Product.objects.create(
            name='Burger', description='Pyszny', price=20.00, category=self.category
        )

    def test_create_order(self):
        response = self.client.post('/api/orders/', {
            "status": "pending",
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity": 2
                }
            ],
            "details": {
                "delivery_notes": "Szybko",
                "delivery_address": "Testowa 123",
                "phone_number": "123456789"
            }
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_order_permission(self):
        other_user = User.objects.create_user(username='other', password='testpass')
        order = Order.objects.create(user=self.user)
        self.client.logout()
        self.client.login(username='other', password='testpass')

        response = self.client.get(f'/api/orders/{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
