from django.db import models

from participants.models import Participant
from paper.models import Paper

class Rating(models.Model):
    paper = models.ForeignKey(Paper)
    rater = models.ForeignKey(Participant, blank=True, null=True)
    score = models.FloatField()
    before = models.BooleanField(default=True)
    
    def __unicode__(self):
        time = "Before" if self.before else "After"
        name = self.rater.name if self.rater else ''
        pattern = "{paper}: {score} ({before})"
        if self.rater: pattern += " - {name}"

        return pattern.format(paper=self.paper.title,
            score=self.score, before=time, name=name)
