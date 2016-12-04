from django.db import models

from paper.models import Paper

class Location(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

class Session(models.Model):
    day = models.DateField()
    location = models.ForeignKey(Location, blank=True, null=True)
    paper = models.ManyToManyField(Paper)
    
    class Meta:
        ordering = ('-day', )
        
    def getPapers(self):
        return [x for x in self.paper.all()]


    #
    # def __unicode__(self):
    #     return "{}: {}".format(self.day.strftime("%d-%m-%Y"), self.location)
