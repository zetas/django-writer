from django.db import models
# Create your models here.


class EmailTemplate(models.Model):
    name = models.CharField(max_length=100)
    verbose_name = models.CharField(max_length=150, verbose_name='Email Template Name')
    type = models.CharField(max_length=50)
    last_modified = models.DateTimeField(auto_now=True)
    html = models.BooleanField(default=False)
    content = models.TextField()

    def __str__(self):
        return self.name

    def get_body(self):
        return self.content.__str__()

    class Meta:
        verbose_name = "Email Template"
        verbose_name_plural = "Email Templates"
