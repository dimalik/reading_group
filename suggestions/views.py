import json

from django.shortcuts import render, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse

from suggestions.models import Suggestion
from suggestions.forms import SuggestionCreateForm

from suggestions.refs import (
    getDoi, getRef, DoiNotFound, RefNotFound
)

get_file_path = lambda x: settings.MEDIA_ROOT + str(x.file)

class SuggestionsHome(ListView):
    template_name = "suggestions/index.html"
    context_object_name = "suggestions"
    model = Suggestion
    paginate_by = 5
    
def download_pdf(request, pid):
    suggestion = Suggestion.objects.get(pk=pid)
    file_ = get_file_path(suggestion)
    with open(file_, 'r') as pdf:
        response = HttpResponse(pdf.read(), mimetype="application/pdf")
        response["Content-Disposition"] = 'attachment'
        return response
    pdf.closed


class SuggestionCreate(CreateView):
    model = Suggestion
    template_name = "suggestions/create.html"
    form_class = SuggestionCreateForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.uploader = self.request.user
        obj.save()
        return HttpResponseRedirect(reverse('edit_doi', kwargs={'pid': obj.pk}))

def edit_doi(request, pid):
    paper = Suggestion.objects.get(pk=pid)
    doi = None
    try:
        doi = getDoi(get_file_path(paper))
    except DoiNotFound:
        return HttpResponseRedirect(reverse('enter_details', kwargs={'pid': paper.pk}))
    
    ref = None
    try:
        ref = getRef(doi)
    except RefNotFound:
        return HttpResponseRedirect(reverse('enter_details', kwargs={'pid': paper.pk}))

    rdict = {}
    try:
        rdict['title'] = ref['title']
    except KeyError:
        title = ''
    try:
        rdict['journal'] = ref['container-title']
    except KeyError:
        journal = ''
    try:
        rdict['volume'] = ref['volume']
    except KeyError:
        volume = ''
    try:
        rdict['issue'] = ref['issue']
    except KeyError:
        issue = ''
    try:
        rdict['year'] = ref['issued']['date-parts'][0][0]
    except KeyError:
        year = ''
    try:
        rdict['authors'] = ["{} {}".format(author['given'], author['family']) for author in ref['author']]
    except KeyError:
        authors = ''
    return render_to_response("suggestions/edit_doi.html", rdict)

def enter_details(request, pid):
    return HttpResponse("temp")
