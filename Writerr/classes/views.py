import json

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.views.generic import UpdateView, DeleteView, ListView, DetailView
from django.views.generic.base import View

from classes.models import Classroom, Attendance, PendingStudents
from classes.forms import ClassForm, ClassFormStep2
from classes.utils import process_students, add_students


class ClassCreate(View):
    template_name = 'classes/classroom_create.html'
    form_class = ClassForm
    form_class_step2 = ClassFormStep2

    def get(self, request, *args, **kwargs):
        request.session['class_confirm'] = False
        return render(request, self.template_name, {'form': self.form_class(), 'step': 1})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        step = kwargs.get('step', 1)
        if form.is_valid():
            students = form.cleaned_data['students']
            student_data = process_students(students)

            student_users = student_data['student_users']
            student_nonusers = student_data['student_nonusers']

            if step == 1:
                return render(request, self.template_name,
                              {
                                  'form': self.form_class_step2(request.POST),
                                  'step': 2,
                                  'student_users': student_users,
                                  'student_nonusers': student_nonusers
                              })
            else:

                classroom = Classroom.objects.create(name=form.cleaned_data['name'])
                user = request.user
                Attendance.objects.create(classroom=classroom, user=user, instructor=True)

                #Big execute
                add_students(classroom, user, student_users, student_nonusers)

                return redirect('account:index')

        return render(request, self.template_name, {'form': form})


class ClassList(ListView):
    context_object_name = 'class_list'

    def get_queryset(self):
        return Classroom.objects.filter(attendance__user=self.request.user)


class ClassView(DetailView):
    model = Classroom
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_queryset(self):
        return Classroom.objects.filter(attendance__user=self.request.user)


class ClassUpdate(UpdateView):
    model = Classroom
    fields = ['name', 'students']
    form_class = ClassForm

    def get_context_data(self, **kwargs):
        context = super(ClassUpdate, self).get_context_data(**kwargs)
        context['pending_students'] = PendingStudents.objects.filter(classroom=self.object)

        return context

    def get_queryset(self):
        return Classroom.objects.filter(attendance__user=self.request.user, attendance__instructor=True)

    def form_valid(self, form):
        if form.cleaned_data['students'] != '':
            student_data = process_students(form.cleaned_data['students'])
            add_students(self.object, self.request.user, student_data['student_users'], student_data['student_nonusers'])

        form.cleaned_data['students'] = self.object.students

        return super(ClassUpdate, self).form_valid(form)


class ClassDelete(DeleteView):
    model = Classroom
    success_url = reverse_lazy('classes:create')

    def get_queryset(self):
        return Classroom.objects.filter(attendance__user=self.request.user, attendance__instructor=True)

    def dispatch(self, *args, **kwargs):
        # maybe do some checks here for permissions ...

        resp = super(ClassDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp


