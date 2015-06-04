__author__ = 'David'

from account.models import WUser, License
from main.utils import send_writerr_email
from classes.models import Attendance, PendingStudents


def _create_pending_student(classroom, email, context, user=None):
    email_template_class_assign_nolic = 'classes.assign_nolic'
    email_template_class_assign_noacct = 'classes.assign_noacct'

    PendingStudents.objects.create(classroom=classroom, email=email, student=user)
    if user is None:
        template = email_template_class_assign_noacct
    else:
        template = email_template_class_assign_nolic

    send_writerr_email('Class Assignment Pending', [email, ], template, context)


def _create_student(classroom, context, user):
    email_template_class_assign = 'classes.assign'

    Attendance.objects.create(classroom=classroom, user=user)
    send_writerr_email('Class Assigned', [user.email, ], email_template_class_assign, context)


def process_students(raw_student_list):
    student_list = raw_student_list.split(',')

    student_users = []
    student_nonusers = []

    for student in student_list:
        s = student.strip()

        try:
            user = WUser.objects.get(email=s)
            student_users.append(user)
        except WUser.DoesNotExist:
            student_nonusers.append(s)

    return {'student_users': student_users, 'student_nonusers': student_nonusers}


def add_students(classroom, instructor, student_users, student_nonusers):
    email_template_new_user = 'account.assigned_new'
    email_template = 'account.assigned'

    licenses = instructor.get_unassigned_licenses()

    if len(licenses) > 0:
        license_list = list(licenses)
    else:
        license_list = None

    for suser in student_users:
        assigned_context = {
            'shortName': suser.get_short_name(),
            'instructorName': instructor.get_short_name(),
            'className': classroom.name
        }
        if not suser.get_license_status():
            if license_list is not None:
                license = license_list.pop(0)
                license.assign(suser)
                license_context = {
                    'shortName': suser.get_short_name(),
                    'purchaser': license.purchasing_user.get_full_name()
                }
                send_writerr_email('New License Assigned', [suser.email, ], email_template, license_context)
                _create_student(classroom, assigned_context, suser)
            else:
                _create_pending_student(classroom, suser.email, assigned_context, suser)
        else:
            _create_student(classroom, assigned_context, suser)

    for semail in student_nonusers:
        e = semail.strip()

        assigned_context = {
            'shortName': e.split('@')[0],
            'instructorName': instructor.get_short_name(),
            'className': classroom.name
        }

        try:
            sent_lic = License.objects.get(sent_to=e)
        except License.DoesNotExist:
            sent_lic = False

        if not sent_lic:
            if license_list is not None:
                license = license_list.pop(0)
                license.sent_to = e
                license.save()
            else:
                license = None
        else:
            license = sent_lic

        if license is not None:
            license_context = {
                'shortName': e.split('@')[0],
                'purchaser': license.purchasing_user.get_full_name(),
                'code': license.redemption_code
            }

            subject = license.purchasing_user.get_short_name()+' has bought you a license!'

            send_writerr_email(subject, [e, ], email_template_new_user, license_context)

        _create_pending_student(classroom, e, assigned_context)