from dataclasses import fields
from django.forms import ValidationError
from rest_framework import serializers
from .models import Books, Teachers, Students

class TeachersSerializer(serializers.ModelSerializer):
  class Meta:
    model = Teachers
    fields = '__all__'
  def validate_age(self, value):
    if int(value) <= 16:
      raise ValidationError('Age should be over 16, as it is not allowed to work teenagers')
    return value
  
class StudentsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Students
    fields = '__all__'
  def validate_age(self, value):
    if int(value) < 12:
      raise ValidationError('Students should be over 12')
    return value

class BooksSerializer(serializers.ModelSerializer):
  # teachers = TeachersSerializer()
  # students = StudentsSerializer()
  class Meta:
    model = Books
    fields = '__all__'

