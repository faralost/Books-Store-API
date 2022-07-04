from django.urls import path, include
from rest_framework import routers

from api_v1.views import BookViewSet, UserBookRelationView

app_name = 'api_v1'

router = routers.DefaultRouter()
router.register('book', BookViewSet)
router.register('book_relation', UserBookRelationView)

urlpatterns = [
    path('', include(router.urls)),
]
