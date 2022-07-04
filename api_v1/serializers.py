from rest_framework import serializers

from store.models import Book, UserBookRelation, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class BookSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(read_only=True, max_digits=3, decimal_places=2)
    discounted_price = serializers.DecimalField(read_only=True, max_digits=7, decimal_places=2)
    owner_name = serializers.CharField(read_only=True)
    readers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'name', 'price', 'author_name', 'likes_count', 'rating', 'discounted_price', 'owner_name', 'readers'
        )


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'is_liked', 'is_bookmarked', 'rate',)
