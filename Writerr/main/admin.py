from django.contrib import admin

# Register your models here.
from main.models import EmailTemplate


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('verbose_name', 'type', 'html', 'last_modified')
    list_filter = ('type', 'html', 'last_modified')
    search_fields = ('verbose_name', )
    ordering = ('type', 'verbose_name', 'html', 'last_modified')

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('verbose_name', 'name', 'type', 'html')
        return self.readonly_fields

    def get_actions(self, request):
        actions = super(EmailTemplateAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(EmailTemplate, EmailTemplateAdmin)