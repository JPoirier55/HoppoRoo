from django.test import TestCase
from HLS.models import Student, Quiz, PDFQuiz, Device, Results


class StudentTestCase(TestCase):
    def setup(self):
        Student.objects.create(name="test",)

