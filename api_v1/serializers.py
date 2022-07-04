from rest_framework import serializers

from store.models import Book, UserBookRelation


class BookSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(read_only=True, max_digits=3, decimal_places=2)
    discounted_price = serializers.DecimalField(read_only=True, max_digits=7, decimal_places=2)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name', 'likes_count', 'rating', 'discounted_price')


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'is_liked', 'is_bookmarked', 'rate',)
