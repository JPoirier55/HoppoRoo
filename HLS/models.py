from __future__ import unicode_literals

from django.db import models

class Quiz(models.Model):
    quizjson = models.TextField(null=True)
    # name = models.CharField(max_length=256)

# class Question(models.Model):
#     question = models.CharField()
#     quiz = models.ForeignKey(Quiz)
#
# class Answer(models.Model):
#     correct = models.CharField()
#

class Device(models.Model):
    id = models.IntegerField(primary_key=True)
    student = models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3)])

class Student(models.Model):
    name = models.CharField(max_length=256)
    id = models.IntegerField(primary_key=True)

# class Grades(models.Model):
#     studentId = models.ForeignKey(Student.id)
