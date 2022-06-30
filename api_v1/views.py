from rest_framework import viewsets

from api_v1.serializers import BookSerializer
from store.models import Book


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
