import json
import collections

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.forms.formsets import formset_factory
from django.views.generic import View
from django.contrib.auth.models import User
from django.conf import settings

from paper.models import Paper, Message
from ratings.models import Rating
from ratings.forms import RatingForm
from participants.models import Participant
from session.models import Session

class PapersHome(TemplateView):
    template_name = 'papers/index.html'
    context_object_name = 'papers'
    
    def get_context_data(self, **kwargs):
        context = super(PapersHome, self).get_context_data(**kwargs)
        context['papers'] = []
        
        for paper in Paper.objects.all().order_by('-session__day'):
            ratings = Rating.objects.filter(paper=paper)           
            
            try:
                before_scores = [rating for rating in ratings if rating.before]
                before_score = sum([rating.score for rating in before_scores]) / float(len(before_scores))
            except ZeroDivisionError:
                before_score = 0
            try:
                after_scores = [rating for rating in ratings if not rating.before]
                after_score = sum([rating.score for rating in after_scores]) / float(len(after_scores))
            except ZeroDivisionError:
                after_score = 0
            try:
                score = sum([rating.score for rating in ratings]) / float(len(ratings))
            except ZeroDivisionError:
                score = 0

            context['papers'].append([paper, score, before_score, after_score])
            
        context['session'] = []
        
        return context
        
class SessionHome(ListView):
    model = Session
    template_name = 'sessions/index.html'
    context_object_name = 'sessions'
    paginate_by = 5
        
class PaperDetail(DetailView):
    model = Paper
    context_object_name = 'paper'
    template_name = 'papers/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(PaperDetail, self).get_context_data(**kwargs)
        
        context['msg'] = Message.objects.filter(paper=self.object)
        context['authors'] = self.object.authors.all()
        context['sessions'] = Session.objects.filter(paper=self.object)
        context['participants'] = Participant.objects.all()
        
        form = RatingForm()
        context['form'] = form
        return context
    
    
def add_rating(request):
    if request.method == "POST":
        participant = int(request.POST.getlist('participant')[0])
        paper_id = int(request.POST.getlist('paperid')[0])
        before = request.POST.getlist('before')[0]
        if before == "1":
            before = False
        else:
            before = True
        try:
            score = float(request.POST.getlist('score')[0])
        except:
            score = 0
        participant = Participant.objects.get(pk=participant)
        paper = Paper.objects.get(pk=paper_id)
        
        r = Rating()
        r.paper = paper
        try:
            r.rater = participant
        except:
            pass
        r.score = score
        r.before = before
        r.save()

    return HttpResponse(json.dumps({'ans': 'Your vote has been cast'}), content_type="application/json")
        
def get_data(request):
    if request.is_ajax():
        try:
            paper_id = int(request.GET.get("paper", None))
            paper = Paper.objects.get(pk=paper_id)
            ratings = Rating.objects.filter(paper=paper)
        except TypeError:
            ratings = Rating.objects.all()
        ranges = map(lambda x: (float(x) / 2) if x != 0 else 0, range(11))
        cnt_before = collections.Counter({v: 0 for v in ranges})
        cnt_after = collections.Counter({v: 0 for v in ranges})
        for r in ratings:
            if r.before:
                cnt_before[r.score] += 1
            else:
                cnt_after[r.score] += 1
        ans_before = []
        for x, y in cnt_before.iteritems():
            ans_before.append({'x': x, 'y': y})
        ans_after = []
        for x, y in cnt_after.iteritems():
            ans_after.append({'x': x, 'y': y})
            
        rd = []
        
        for r in ranges:
            rd.append({'pos': r, 'before': cnt_before[r], 'after': cnt_after[r]})

        return HttpResponse(json.dumps(rd), content_type="application/json")
        
def paper_send_message(request, pk):
    if request.POST:
        if request.is_ajax():
            paper = Paper.objects.get(pk=pk)
            message = Message()
            message.user = User.objects.get(username=request.user)
            message.message =  request.POST.get('data', '')
            message.paper = paper
            message.save()
    return HttpResponse(json.dumps({'msg': 'gg'}), content_type="application/json")
    
def download_pdf(request, pid):
    paper = Paper.objects.get(pk=pid)
    file_ = settings.MEDIA_ROOT + str(paper.file)
    filename = "{author} {year} {title}".format(
        author=paper.get_authors(),
        year=paper.year,
        title=paper.title
    )
    with open(file_, 'r') as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment;filename="{}.pdf"'.format(filename)
        return response
    pdf.closed