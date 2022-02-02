from django.urls import path, include
from .views import (
  BooksAPIView,
  BookDetailAPIView, 
  StudentsViewset,
  TeachersViewset,
  BooksViewset,
)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('students', StudentsViewset, basename='students'),
router.register('teachers', TeachersViewset, basename='teachers'),
router.register('books', BooksViewset, basename='books')

urlpatterns = [
    path('books/', BooksAPIView.as_view(), name='books'),
    # path('book/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('', include(router.urls)),
]


