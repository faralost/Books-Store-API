from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_books')
    readers = models.ManyToManyField(User, through='store.UserBookRelation', related_name='rated_books')

    def __str__(self):
        return f'{self.name}'


class UserBookRelation(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    RATE_CHOICES = (
        (ONE, 'OK'),
        (TWO, 'FINE'),
        (THREE, 'GOOD'),
        (FOUR, 'AMAZING'),
        (FIVE, 'INCREDIBLE'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('store.Book', on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    is_bookmarked = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return f'{self.user} | {self.book} | {self.rate}'
