from django.db import models
from django.contrib.auth.models import User

get_title = lambda x: x.split('/')[-1][:-4]

class Suggestion(models.Model):
    
    file = models.FileField(upload_to="suggestions/", max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True, verbose_name="Suggestion notes")
    uploader = models.ForeignKey(User)

    def __unicode__(self):
        if self.title:
            return self.title
        return get_title(self.file.name)
