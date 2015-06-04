from django.contrib import admin

from classes.models import Classroom, Attendance

# Register your models here.


class AttendanceInline(admin.TabularInline):
    model = Attendance
    fk_name = 'classroom'
    extra = 0


class ClassroomAdmin(admin.ModelAdmin):
    inlines = [
        AttendanceInline,
    ]

    list_display = ('name', 'class_code', 'creation')
    list_filter = ('creation', )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', )}
        ),
    )

    fieldsets = (
        (None, {'fields': ('name', 'class_code', 'creation')}),
    )

    search_fields = ('name', 'class_code')
    ordering = ('creation', )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('class_code', 'creation')
        return self.readonly_fields

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(ClassroomAdmin, self).get_fieldsets(request, obj)

admin.site.register(Classroom, ClassroomAdmin)