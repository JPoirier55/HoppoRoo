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
