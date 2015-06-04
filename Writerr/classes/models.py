from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse

from account.models import WUser
from account.utils import _create_small_code

# Create your models here.


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, default=_create_small_code)
    students = models.ManyToManyField(WUser, through='Attendance')
    creation = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def class_code(self):
        full_code = "%s-%s" % (self.name, self.code)
        return slugify(unicode(full_code)).__str__()

    def get_absolute_url(self):
        return reverse('classes:update', kwargs={'pk': self.pk})

    def get_instructors(self):
        return self.students.filter(attendance__instructor=True)
    instructors = property(get_instructors)


class Attendance(models.Model):
    user = models.ForeignKey(WUser)
    classroom = models.ForeignKey(Classroom)
    instructor = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s in %s" % (self.user, self.classroom)


class PendingStudents(models.Model):
    classroom = models.ForeignKey(Classroom)
    student = models.ForeignKey(WUser, blank=True, null=True)
    email = models.EmailField()
    creation = models.DateTimeField(auto_now_add=True)



