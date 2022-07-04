from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_books')
    readers = models.ManyToManyField(User, through='store.UserBookRelation', related_name='rated_books')
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)

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
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__rate = self.rate

    def __str__(self):
        return f'{self.user} | {self.book} | {self.rate}'

    def save(self, *args, **kwargs):
        from api_v1.logic import set_rating

        creating_now = not self.pk

        super().save(*args, **kwargs)

        new_rating = self.rate

        if self.__rate != new_rating or creating_now:
            set_rating(self.book)

        self.__rate = self.rate
