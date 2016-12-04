# -*- coding: utf-8 -*-
import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User

from sortedm2m.fields import SortedManyToManyField

import session

def update_filename(instance, filename):
    path = "papers/"
    ext = filename.split('.')[-1]
    format_ = "{}.{}".format(str(uuid4()), ext)
    path += format_
    return path
    
class Message(models.Model):
    user = models.ForeignKey(User)
    message = models.TextField()
    paper = models.ForeignKey("Paper")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "{}: {}".format(self.user, self.message[:40])
    
class Affiliation(models.Model):
    department = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    post_details = models.CharField(max_length=50, blank=True)
    
    def __unicode__(self):
        return u"{} - {}".format(self.department, self.university)

class Author(models.Model):
    name = models.CharField(max_length=255)
    affiliation = models.ManyToManyField(Affiliation, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
    
class Journal(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    
    class Meta:
        ordering = ('title',)
    
    def __unicode__(self):
        return self.title

class Paper(models.Model):
    title = models.CharField(max_length=255)
    authors = SortedManyToManyField(Author)
    journal = models.ForeignKey(Journal)
    file = models.FileField(upload_to=update_filename, max_length=255,
                            blank=True, null=True)
    year = models.IntegerField(max_length=4)
    volume = models.IntegerField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    pages = models.CharField(max_length=16, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    related_papers = models.ManyToManyField("self", blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    open_for_voting = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return ('papers_paperdetail_view', (), {'pk': self.pk})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_sessions(self):
        return session.models.Session.objects.filter(paper=self)
        
    def get_authors(self):
        return ", ".join([author.name for author in self.authors.all()])
        
    def get_authors_min(self):
        if len(self.authors.all()) > 1:
            return "{author} et al.".format(
                author=self.authors.first().name.split()[-1].encode('utf-8'))
        return self.authors.first()
