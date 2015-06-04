from django.contrib import admin

# Register your models here.
from papers.models import Paper, PaperSubmission, PaperComment


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'paper', 'slug', 'submitted_to', 'date_submitted')
    list_filter = ('date_submitted', )
    search_fields = ('submitted_to', 'slug')
    ordering = ('paper', 'submitted_to', 'date_submitted')

    def has_add_permission(self, request):
        return False


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'paper', 'created')
    list_filter = ('created', )
    search_fields = ('author', 'paper')


admin.site.register(Paper)
admin.site.register(PaperComment, CommentAdmin)
admin.site.register(PaperSubmission, SubmissionAdmin)