from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from paper.models import Paper

def update_filename(instance, filename):
    path = "images/"
    ext = filename.split('.')[-1]
    format_ = "{}_{}.{}".format(instance.get_authors(), instance.year, ext)
    return os.path.join(path, format_)


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    author = models.ForeignKey(User)
    paper = models.ForeignKey(Paper)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=update_filename, blank=True, null=True)
    
    def __unicode__(self):
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('blog_post_detail', (), 
                {
                    'slug' :self.slug,
                })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)