from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api_v1.serializers import BookSerializer
from store.models import Book


class BookApiTestCase(APITestCase):
    def test_get_list_of_books(self):
        book1 = Book.objects.create(name='Test Book 1', price=100)
        book2 = Book.objects.create(name='Test Book 2', price=200)
        url = reverse('api_v1:book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([book1, book2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
