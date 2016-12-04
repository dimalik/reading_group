from django.forms import ModelForm
from blog.models import Post

class BlogCreateForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('slug', 'paper', 'author',)