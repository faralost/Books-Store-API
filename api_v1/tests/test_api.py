import json

from django.contrib.auth import get_user_model
from django.db.models import Count, Case, When, Avg, ExpressionWrapper, F, DecimalField, Subquery, OuterRef
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from api_v1.serializers import BookSerializer
from store.models import Book, UserBookRelation

User = get_user_model()


class BookApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.book1 = Book.objects.create(name='Test Book 1', price=100, author_name='Author 1', owner=self.user)
        self.book2 = Book.objects.create(name='Test Book 2', price=200, author_name='Author 2')
        self.book3 = Book.objects.create(name='Test Book 3 Author 1', price=100, author_name='Author 3')
        self.url_list = reverse('api_v1:book-list')
        self.url_detail = reverse('api_v1:book-detail', args=(self.book1.id,))
        UserBookRelation.objects.create(user=self.user, book=self.book1, is_liked=True, rate=5)

    def test_get_list_of_books(self):
        response = self.client.get(self.url_list)
        books = Book.objects.annotate(
            likes_count=Count(Case(When(userbookrelation__is_liked=True, then=1))),
            discounted_price=ExpressionWrapper(F('price') - F('discount'), output_field=DecimalField()),
            owner_name=Subquery(User.objects.filter(id=OuterRef('owner_id')).values('username'))
        ).order_by('pk')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['rating'], '5.00')
        self.assertEqual(serializer_data[0]['likes_count'], 1)

    def test_get_list_of_filtered_books_by_price(self):
        response = self.client.get(self.url_list, data={'price': 100})
        books = Book.objects.filter(id__in=[self.book1.id, self.book3.id]).annotate(
            likes_count=Count(Case(When(userbookrelation__is_liked=True, then=1))),
            discounted_price=ExpressionWrapper(F('price') - F('discount'), output_field=DecimalField()),
            owner_name=Subquery(User.objects.filter(id=OuterRef('owner_id')).values('username'))
        ).order_by('pk')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_of_searched_books_by_name_and_author_name(self):
        response = self.client.get(self.url_list, data={'search': 'Author 1'})
        books = Book.objects.filter(id__in=[self.book1.id, self.book3.id]).annotate(
            likes_count=Count(Case(When(userbookrelation__is_liked=True, then=1))),
            discounted_price=ExpressionWrapper(F('price') - F('discount'), output_field=DecimalField()),
            owner_name=Subquery(User.objects.filter(id=OuterRef('owner_id')).values('username'))
        ).order_by('pk')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_of_ordered_books_by_author_name_descending(self):
        response = self.client.get(self.url_list, data={'ordering': '-author_name'})
        books = Book.objects.filter(id__in=[self.book1.id, self.book2.id, self.book3.id]).annotate(
            likes_count=Count(Case(When(userbookrelation__is_liked=True, then=1))),
            discounted_price=ExpressionWrapper(F('price') - F('discount'), output_field=DecimalField()),
            owner_name=Subquery(User.objects.filter(id=OuterRef('owner_id')).values('username'))
        ).order_by('-author_name', 'id')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_of_ordered_books_by_price_ascending(self):
        response = self.client.get(self.url_list, data={'ordering': 'price'})
        books = Book.objects.filter(id__in=[self.book1.id, self.book2.id, self.book3.id]).annotate(
            likes_count=Count(Case(When(userbookrelation__is_liked=True, then=1))),
            discounted_price=ExpressionWrapper(F('price') - F('discount'), output_field=DecimalField()),
            owner_name=Subquery(User.objects.filter(id=OuterRef('owner_id')).values('username'))
        ).order_by('price', 'id')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_book(self):
        response = self.client.get(self.url_detail)
        book = Book.objects.annotate(
            likes_count=Count(Case(When(userbookrelation__is_liked=True, then=1))),
            discounted_price=ExpressionWrapper(F('price') - F('discount'), output_field=DecimalField()),
            owner_name=Subquery(User.objects.filter(id=OuterRef('owner_id')).values('username'))
        ).get(id=self.book1.id)
        serializer_data = BookSerializer(book).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_book_that_doesnt_exists(self):
        self.url_detail = reverse('api_v1:book-detail', args=(34,))
        response = self.client.get(self.url_detail)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_create_book(self):
        self.assertEqual(3, Book.objects.all().count())
        data = {
            'name': 'New Book of Pyhon 3',
            'price': 666,
            'author_name': 'Irina Lesnikova'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(self.url_list, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        new_book = Book.objects.get(id=4)
        self.assertEqual('New Book of Pyhon 3', new_book.name)
        self.assertEqual(666, new_book.price)
        self.assertEqual(self.user, new_book.owner)

    def test_update_book(self):
        data = {
            'name': self.book1.name,
            'price': 666,
            'author_name': self.book1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(self.url_detail, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(666, self.book1.price)

    def test_update_book_by_not_owner(self):
        self.user2 = User.objects.create(username='testuser2')
        data = {
            'name': self.book1.name,
            'price': 666,
            'author_name': self.book1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(self.url_detail, data=json_data, content_type='application/json')
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(100, self.book1.price)

    def test_update_book_by_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='testuser2', is_staff=True)
        data = {
            'name': self.book1.name,
            'price': 666,
            'author_name': self.book1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(self.url_detail, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(666, self.book1.price)

    def test_delete_book(self):
        self.assertEqual(3, Book.objects.all().count())
        self.client.force_login(self.user)
        response = self.client.delete(self.url_detail)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())

    def test_delete_book_by_not_owner(self):
        self.user2 = User.objects.create(username='testuser2')
        self.assertEqual(3, Book.objects.all().count())
        self.client.force_login(self.user2)
        response = self.client.delete(self.url_detail)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, Book.objects.all().count())

    def test_delete_book_by_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='testuser2', is_staff=True)
        self.assertEqual(3, Book.objects.all().count())
        self.client.force_login(self.user2)
        response = self.client.delete(self.url_detail)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())


class UserBookRelationApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user2 = User.objects.create(username='testuser2')
        self.book1 = Book.objects.create(name='Test Book 1', price=100, author_name='Author 1', owner=self.user)
        self.book2 = Book.objects.create(name='Test Book 2', price=200, author_name='Author 2')
        self.url = reverse('api_v1:userbookrelation-detail', args=(self.book1.id,))

    def test_like(self):
        data = {
            'is_liked': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)
        self.assertTrue(relation.is_liked)

    def test_unlike(self):
        relation = UserBookRelation.objects.create(user=self.user, book=self.book1, is_liked=True)
        data = {
            'is_liked': False,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(self.url, data=json_data, content_type='application/json')
        relation.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertFalse(relation.is_liked)

    def test_rate(self):
        data = {
            'rate': 4,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)
        self.assertEqual(4, relation.rate)

    def test_rate_wrong(self):
        data = {
            'rate': 7,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)
        self.assertEqual(None, relation.rate)
