from django.db.models import Count, Case, When, Avg, ExpressionWrapper, F, DecimalField, Prefetch, Subquery, OuterRef
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api_v1.permissions import IsOwnerOrStaffOrReadOnly
from api_v1.serializers import BookSerializer, UserBookRelationSerializer
from store.models import Book, UserBookRelation, User


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.annotate(
        likes_count=Count(Case(When(userbookrelation__is_liked=True, then=1))),
        discounted_price=ExpressionWrapper(F('price') - F('discount'), output_field=DecimalField()),
        owner_name=Subquery(User.objects.filter(id=OuterRef('owner_id')).values('username'))
    ).prefetch_related(
        Prefetch('readers', queryset=User.objects.all().distinct().only('id', 'first_name', 'last_name'))
    ).order_by('pk')
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    queryset = UserBookRelation.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, created = UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])
        return obj


def oauth(request):
    return render(request, 'api/oauth.html')
