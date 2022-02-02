from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class MyPagePagination(PageNumberPagination):
  page_size = 3 

