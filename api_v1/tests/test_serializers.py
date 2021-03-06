from django.db.models import Count, Case, When, Avg, ExpressionWrapper, F, DecimalField, Subquery, OuterRef
from django.test import TestCase

from api_v1.serializers import BookSerializer
from store.models import Book, User, UserBookRelation


class BookSerializerTestCase(TestCase):
    def test_serializer_is_ok(self):
        user1 = User.objects.create(username='user1', first_name='user1', last_name='userov1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')

        book1 = Book.objects.create(name='Test Book 1', price=100, author_name='Author 1', discount=50)
        book2 = Book.objects.create(name='Test Book 2', price=200, author_name='Author 2', owner=user1)

        UserBookRelation.objects.create(user=user1, book=book1, is_liked=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book1, is_liked=True, rate=5)
        user_book = UserBookRelation.objects.create(user=user3, book=book1, is_liked=True)
        user_book.rate = 4
        user_book.save()

        UserBookRelation.objects.create(user=user1, book=book2, is_liked=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=book2, is_liked=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book2, is_liked=False)

        books = Book.objects.annotate(
            likes_count=Count(Case(When(userbookrelation__is_liked=True, then=1))),
            discounted_price=ExpressionWrapper(F('price') - F('discount'), output_field=DecimalField()),
            owner_name=Subquery(User.objects.filter(id=OuterRef('owner_id')).values('username'))
        ).order_by('pk')

        data = BookSerializer(books, many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test Book 1',
                'price': '100.00',
                'author_name': 'Author 1',
                'likes_count': 3,
                'rating': '4.67',
                'discounted_price': '50.00',
                'owner_name': None,
                'readers': [
                    {
                        'id': user1.id,
                        'first_name': 'user1',
                        'last_name': 'userov1'
                    },
                    {
                        'id': user2.id,
                        'first_name': '',
                        'last_name': ''
                    },
                    {
                        'id': user3.id,
                        'first_name': '',
                        'last_name': ''
                    }
                ]

            },
            {
                'id': book2.id,
                'name': 'Test Book 2',
                'price': '200.00',
                'author_name': 'Author 2',
                'likes_count': 2,
                'rating': '3.50',
                'discounted_price': '200.00',
                'owner_name': 'user1',
                'readers': [
                    {
                        'id': user1.id,
                        'first_name': 'user1',
                        'last_name': 'userov1'
                    },
                    {
                        'id': user2.id,
                        'first_name': '',
                        'last_name': ''
                    },
                    {
                        'id': user3.id,
                        'first_name': '',
                        'last_name': ''
                    }
                ]
            },
        ]
        self.assertEqual(expected_data, data)
