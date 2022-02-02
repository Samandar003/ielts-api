from django.db import models
from django.contrib.auth import get_user_model


class Students(models.Model):
  LEVEL = (
    ('BEGINNER', 'Beginner'),
    ('PRE-IELTS', 'Pre-ielts'),
    ('IELTS', 'Ielts'),
    ('FOUNDATION', 'Foundation'),
    ('GRADUATION', 'Graduation'),
  )
  
  first_name  = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  age = models.PositiveSmallIntegerField(default=12)
  level = models.CharField(max_length=20, choices=LEVEL, default=LEVEL[0][0])
 
  def __str__(self):
    full_name = f"{self.first_name} {self.last_name}"
    return full_name

class Teachers(models.Model):
  BAND_SCORE = [
    ('+6.5 score', '+6.5 score'),
    ('+7.0 score', '+7.0 score'),
    ('+7.5 score', '+7.5 score'),
    ('+8.0 score', '+8.0 score'),
    ('+8.5 score', '+8.5 score'),
    ('+9.0 score', '+9.0 score'),
  ]
  first_name  = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  # ielts_level = models.PositiveSmallIntegerField(default=7)
  ielts_level = models.CharField(max_length=20, choices=BAND_SCORE, default=BAND_SCORE[1][0])
  age = models.PositiveSmallIntegerField(default=16)

  def __str__(self):
    full_name = f"{self.first_name} {self.last_name}"
    return full_name

class Books(models.Model):
  SECTION = (
    ('READING', 'Reading'),
    ('LISTENING', 'Listening'),
    ('WRITING', 'Writing'),
    ('SPEAKING', 'Speaking'),
    ('FULL', 'Full'),
  )
  
  title = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  section = models.CharField(max_length=20, choices=SECTION, default=SECTION[4][0])
  students = models.ManyToManyField(Students, related_name='students')
  teachers = models.ManyToManyField(Teachers, related_name='teachers')
  read_num = models.PositiveIntegerField(default=0)

  def __str__(self):
    return self.title
  

  
  