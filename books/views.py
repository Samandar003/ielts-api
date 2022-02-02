from django import views
from django.shortcuts import render
from rest_framework.response import Response
from .models import Books, Teachers, Students
from .serializers import BooksSerializer, StudentsSerializer, TeachersSerializer
from rest_framework.views import APIView
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.filters import OrderingFilter
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import mixins
from .mypagination import MyPagePagination


# here I am doing all crud actions with apiview
class BooksAPIView(APIView):
  def get(self, request):
    books = Books.objects.all()
    serializer = BooksSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request):
    serializer = BooksSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class BookDetailAPIView(APIView):
  def get(self, request, pk):
    book = Books.objects.get(id=pk)
    serializer = BooksSerializer(book)
    return Response(serializer.data)
  def put(self, request, pk):
    book = Books.objects.get(id=pk)
    serializer = BooksSerializer(book, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
  def delete(self, request, pk):
    book = Books.objects.get(id=pk)
    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# here I am using modelviewset and it makes easy all crud actions
class StudentsViewset(viewsets.ModelViewSet):
  queryset = Students.objects.all()
  serializer_class = StudentsSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  pagination_class = LimitOffsetPagination
  filter_backends = [filters.OrderingFilter]
  ordering_fields = ['age', '-age']
  search_fields = ['first_name', 'last_name', 'age']
  queryset = Students.objects.all()
  def get_queryset(self):
    queryset = Students.objects.all()
    query = self.request.query_params.get('search')
    if query:
      queryset = Students.objects.annotate(
        similarity=TrigramSimilarity('first_name', query)
      ).filter(similarity__gt=0.2).order_by('-similarity')
    return queryset
   
 
class TeachersViewset(viewsets.ModelViewSet):
  queryset = Teachers.objects.all()
  serializer_class = TeachersSerializer
  authentication_classes = [TokenAuthentication,]
  permission_classes = [IsAuthenticated,]
  pagination_class = MyPagePagination
  filter_backends = [filters.SearchFilter, filters.OrderingFilter]
  search_fields = ['first_name', 'last_name', 'age']
  ordering_fields = ['age', '-age']

# it is better way of crud to add action
class BooksViewset(viewsets.ModelViewSet):
  queryset = Books.objects.all()
  serializer_class = BooksSerializer    
  authentication_classes = [TokenAuthentication,]
  permission_classes = [IsAuthenticated,]
  pagination_class = MyPagePagination
  # filter_backends = [filters.SearchFilter]
  # search_fields = ['title', 'students__first_name', 'students__last_name']   

  def get_queryset(self):
    queryset = Books.objects.all()
    query = self.request.query_params.get('search')
    if query is not None:
      queryset = Books.objects.annotate(
        similarity=TrigramSimilarity('title', query)).filter(
          similarity__gt=0.2
        ).order_by('-similarity')
    return queryset

# I am printing students of a particular book
  @action(detail=True, methods=['get'])
  def students(self, request, *args, **kwargs):
    book = self.get_object()
    serializer = StudentsSerializer(book.students, many=True)
    return Response(serializer.data)

  @action(detail=True, methods=['post'])
  def add_students(self, request, *args, **kwargs):
    book = self.get_object()
    student = Students.objects.get(id=request.data.get('id'))
    book.students.add(student)
    serializer = BooksSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @action(detail=True, methods=['POST'])
  def remove_students(self, request, *args, **kwargs):
    book = self.get_object()
    student = Students.objects.get(id=request.data.get('id'))
    book.students.remove(student)
    return Response(status=status.HTTP_204_NO_CONTENT)

  @action(detail=True, methods=['GET'])
  def teachers(self, request, *args, **kwargs):
    book = self.get_object()
    serializer = TeachersSerializer(book.teachers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK) 
  
  @action(detail=True, methods=['post'])
  def add_teachers(self, request, *args, **kwargs):
    book = self.get_object()
    teacher = Teachers.objects.get(id=request.data.get('id'))
    book.teachers.add(teacher)
    serializer = BooksSerializer(book)
    return Response(serializer.data)
  
  @action(detail=True, methods=['POST'])
  def remove_teachers(self, request, *args, **kwargs):
    book = self.get_object()
    teacher = Teachers.objects.get(id=request.data.get('id'))
    book.teachers.remove(teacher)
    return Response(status=status.HTTP_204_NO_CONTENT)   
  
  @action(detail=True, methods=['post'])
  def read(self, request, *args, **kwargs):
    book = self.get_object()
    with transaction.atomic():
      book.read_num += 1
      book.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
  @action(detail=False, methods=['GET'])
  def top(self, request, *args, **kwargs):
    books = self.get_queryset()
    books = books.order_by('-read_num')[:10]
    serializer = BooksSerializer(books, many=True)
    return Response(serializer.data)
  
