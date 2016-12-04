from django.db import models

class Participant(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['name',]
    
    def __unicode__(self):
        return self.name
