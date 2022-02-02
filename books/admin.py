from django.contrib import admin
from .models import Books, Teachers, Students

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
  list_display = ['id', 'title']


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
  list_display = ['id', 'first_name', 'last_name', 'age', 'level']
  list_filter = ['age']

  
@admin.register(Teachers)
class TeachersAdmin(admin.ModelAdmin):
  list_display = ['id', 'first_name', 'last_name', 'age', 'ielts_level']
  list_filter = ['age']
