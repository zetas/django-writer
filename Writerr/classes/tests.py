import random

from django.test import TestCase
from django.utils.text import slugify

from account.models import WUser
from classes.models import Classroom, Attendance

# Create your tests here.


def create_user():
    email = random.randint(0, 100000).__str__()+'test@example.com'
    return WUser.objects.create_user(email=email, password='testpassword')


class ClassesModelTests(TestCase):

    def test_classroom_model_creation(self):
        """
        Be sure the classroom model is able to be created properly.
        """
        room = Classroom(name='Cool new Class')
        room.save()
        self.assertIsInstance(room, Classroom)

    def test_classroom_code_output(self):
        """
        Test code generation.
        """
        class_name = 'Cool new Class'
        room = Classroom(name=class_name)
        room.save()

        full_code = "%s-%s" % (class_name, room.code)

        self.assertEqual(room.get_full_code(), slugify(unicode(full_code)).__str__())

    def test_classroom_association(self):
        """
        Test the intermediary model is working as intended
        """
        instructor = create_user()

        room = Classroom.objects.create(name='Relationship Test')

        attendance = Attendance(user=instructor, classroom=room, instructor=True)
        attendance.save()

        classes = instructor.classroom_set.all()

        self.assertEqual(classes[0].name, 'Relationship Test')


