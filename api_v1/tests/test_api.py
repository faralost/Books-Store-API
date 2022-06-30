from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api_v1.serializers import BookSerializer
from store.models import Book


class BookApiTestCase(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(name='Test Book 1', price=100, author_name='Author 1')
        self.book2 = Book.objects.create(name='Test Book 2', price=200, author_name='Author 2')
        self.book3 = Book.objects.create(name='Test Book 3 Author 1', price=100, author_name='Author 3')
        self.url = reverse('api_v1:book-list')

    def test_get_list_of_books(self):
        response = self.client.get(self.url)
        serializer_data = BookSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_of_filtered_books_by_price(self):
        response = self.client.get(self.url, data={'price': 100})
        serializer_data = BookSerializer([self.book1, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_of_searched_books_by_name_and_author_name(self):
        response = self.client.get(self.url, data={'search': 'Author 1'})
        serializer_data = BookSerializer([self.book1, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_of_ordered_books_by_author_name_descending(self):
        response = self.client.get(self.url, data={'ordering': '-author_name'})
        serializer_data = BookSerializer([self.book3, self.book2, self.book1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_of_ordered_books_by_price_ascending(self):
        response = self.client.get(self.url, data={'ordering': 'price'})
        serializer_data = BookSerializer([self.book1, self.book3, self.book2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
