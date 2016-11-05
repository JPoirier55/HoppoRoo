"""
    Django unit tests for database input

    Author: Jake Poirier
    Date: 11/4/16
"""

from django.test import TestCase
from HLS.models import Student, Quiz, PDFQuiz, Device, Results


class StudentTestCase(TestCase):
    def setUp(self):
        Student.objects.create(name="test_man1", id=1)
        Student.objects.create(name="test_man2", id=2)
        Student.objects.create(name="test_man3", id=3)

    def test_student_name(self):
        t1 = Student.objects.get(name='test_man1')
        t2 = Student.objects.get(name='test_man2')
        t3 = Student.objects.get(name='test_man3')
        self.assertEqual(t1.id, 1)
        self.assertEqual(t2.id, 2)
        self.assertEqual(t3.id, 3)


class QuizTestCase(TestCase):
    def setUp(self):
        Quiz.objects.create(name="test_quiz1", id=1, quizjson="{\"blah\": 45}", subject='Math')
        Quiz.objects.create(name="test_quiz2", id=2, quizjson="{}", subject='Science')
        Quiz.objects.create(name="test_quiz3", id=3, quizjson="{}", subject='Math')

    def test_quiz_subject(self):
        q1 = Quiz.objects.get(name='test_quiz1')
        q2 = Quiz.objects.get(id=2)
        q3 = Quiz.objects.get(name='test_quiz3')

        self.assertEqual(q1.subject, 'Math')
        self.assertEqual(q2.subject, 'Science')
        self.assertEqual(q3.subject, 'Math')

    def test_quiz_id(self):
        q1 = Quiz.objects.get(name='test_quiz1')
        q2 = Quiz.objects.get(id=2)
        q3 = Quiz.objects.get(name='test_quiz3')

        self.assertEqual(q1.id, 1)
        self.assertEqual(q2.id, 2)
        self.assertEqual(q3.id, 3)

    def test_quizjson(self):
        q1 = Quiz.objects.get(name='test_quiz1')
        self.assertEqual(q1.quizjson, "{\"blah\": 45}")


class DeviceTestCase(TestCase):
    def setUp(self):
        Student.objects.create(name='test_man1', id=5)
        t1 = Student.objects.get(name="test_man1")
        Device.objects.create(id=1, student=t1)

    def test_device_link(self):
        d1 = Device.objects.get(id=1)
        self.assertEqual(d1.student.name, "test_man1")
        t1 = Student.objects.get(name="test_man1")
        d2 = Device.objects.get(student=t1)
        self.assertEqual(d2.student.id, 5)
