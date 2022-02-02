from django.test import TestCase, SimpleTestCase, Client
from django.urls import resolve, reverse
from books.views import BooksAPIView
from books.models import Students

class UrlsTest(TestCase):
  def setUp(self) -> None:
      self.client = Client()
      self.student1 = Students.objects.create(first_name='aaaaa', 
                    last_name='bbbb', level='BEGINNER', age=20)
      self.student2 = Students.objects.create(first_name='panji', 
                    last_name='berdiyev', level='PRE-IELTS', age=24)
      self.student2 = Students.objects.create(first_name='jalol', 
                    last_name='halol', level='IELTS', age=19)
  
  def test_students_url(self):
    url = reverse('books')
    self.assertEquals(resolve(url).func.view_class, BooksAPIView)
    response = self.client.get('/books/')
    data = response.data
    self.assertEquals(response.status_code, 200)
  def test_students(self):
    response = self.client.get('/students/?search=aaaa')
    
    data = response.data
    print(data)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(data), 1)
    self.assertIsNotNone(data[0]['id'])
    self.assertEquals(data[0]['first_name'], 'aaaaa')
  def test_ordering_age(self):
    response = self.client.get('/students/?ordering=-age')
    data = response.data
    print(data)
    self.assertEquals(data[0]['id'], 2)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(data), 3)

