from django.contrib import admin

from store.models import Book, UserBookRelation

admin.site.register(Book)
admin.site.register(UserBookRelation)
