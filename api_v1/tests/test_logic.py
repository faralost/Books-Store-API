from django.test import TestCase

from api_v1.logic import set_rating
from store.models import User, Book, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1', first_name='user1', last_name='userov1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')

        self.book1 = Book.objects.create(name='Test Book 1', price=100, author_name='Author 1', discount=50)

        UserBookRelation.objects.create(user=user1, book=self.book1, is_liked=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=self.book1, is_liked=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=self.book1, is_liked=True, rate=4)

    def test_ok(self):
        set_rating(self.book1)
        self.book1.refresh_from_db()
        self.assertEqual('4.67', str(self.book1.rating))
