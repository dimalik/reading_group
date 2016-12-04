from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from paper.models import Paper
from blog.models import Post
from blog.forms import BlogCreateForm

class BlogHome(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    pagination = 5
    
class BlogPostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    
class BlogPostCreate(CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = BlogCreateForm
    
    def form_valid(self, form):
        paper = Paper.objects.get(pk=int(self.kwargs['pk']))
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.paper = paper
        obj.save()
        return HttpResponseRedirect('/')