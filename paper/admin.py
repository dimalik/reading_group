from django.contrib import admin

from paper.models import Paper, Author, Journal, Affiliation, Message

class PaperAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'get_authors', 'journal', 'year')

admin.site.register(Paper, PaperAdmin)
admin.site.register(Message)
admin.site.register(Author)
admin.site.register(Journal)
admin.site.register(Affiliation)