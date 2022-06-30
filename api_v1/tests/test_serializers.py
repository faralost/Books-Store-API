from django.test import TestCase

from api_v1.serializers import BookSerializer
from store.models import Book


class BookSerializerTestCase(TestCase):
    def test_serializer_is_ok(self):
        book1 = Book.objects.create(name='Test Book 1', price=100)
        book2 = Book.objects.create(name='Test Book 2', price=200)
        data = BookSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test Book 1',
                'price': '100.00'
            },
            {
                'id': book2.id,
                'name': 'Test Book 2',
                'price': '200.00'
            },
        ]
        self.assertEqual(expected_data, data)
