from __future__ import unicode_literals

from django.db import models


class Quiz(models.Model):
    quizjson = models.TextField(null=True)
    name = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=256, default='')
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return "{0} - ID: {1}".format(self.name, self.id)


class Device(models.Model):
    id = models.IntegerField(primary_key=True, default=None)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return "Device: {0} - Linked to {1}".format(self.id, self.student.name)


class Results(models.Model):
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE)
    student = models.OneToOneField(Student)
    score = models.IntegerField(default=0)

    def __str__(self):
        return "Student: {0} - Quiz: {1} - Score: {2}".format(self.student.name, self.quiz.name, self.score)
