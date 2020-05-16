from django.db import models
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
User = get_user_model()


class Student(models.Model):
    class Meta:
        db_table = 'student'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    city = models.CharField(max_length=500, blank=True, null=True)
    grade = models.IntegerField(blank=False, null=False)
    board = models.CharField(max_length=500, blank=False, null=False)


class Question(models.Model):
    class Meta:
        db_table = 'question'
    question = models.TextField(null=False, blank=False)


class Classes(models.Model):
    class Meta:
        db_table = 'classes'
    session = models.CharField(max_length=1000, null=False, blank=False)
    question = models.ManyToManyField(Question, blank=True, null=True)
    date = models.DateField(default=datetime.now()+timedelta(days=30))


class AvailableSessions(models.Model):
    class Meta:
        db_table = 'available_sessions'

    grade = models.IntegerField(blank=False, null=False)
    board = models.CharField(max_length=500, blank=False, null=False)
    classes = models.ManyToManyField(Classes, blank=True , null=False)



