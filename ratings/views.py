import csv
import StringIO

from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson as json
from django.views.generic import UpdateView

from paper.models import Paper
from ratings.models import Rating

def getRatings(request):
    
    ## generate ratings file
    data_file = StringIO.StringIO()
    writer = csv.writer(data_file)
    writer.writerow([
        'paper_id',
        'paper_title',
        'paper_year',
        'paper_journal_id',
        'paper_journal_name',
        'paper_journal_volume',
        'paper_journal_number',
        'paper_no_authors',
        'rater_id',
        'rater_identifier',
        'score',
        'time',
        # 'session',
        # 'session_location',
    ])
    
    for rating in Rating.objects.all():
        paper_id = rating.paper.pk
        paper_title = rating.paper.title
        try:
            paper_year = rating.paper.year
        except AttributeError:
            paper_year = ""
        if not paper_year:
            paper_year = ""
        paper_journal_id = rating.paper.journal.pk
        paper_journal_name = rating.paper.journal.title
        try:
            paper_journal_volume = rating.paper.volume
        except AttributeError:
            paper_journal_volume = ""
        try:
            paper_journal_number = rating.paper.number
        except AttributeError:
            paper_journal_number = ""
        paper_no_authors = len(rating.paper.authors.all())
        try:
            rater_id = rating.rater.pk
            rater_identifier = rating.rater.name[:3]
        except AttributeError:
            rater_id = ""
            rater_identifier = ""
        score = rating.score
        time = 0 if rating.before else 1
        
        writer.writerow([
            paper_id,
            paper_title,
            paper_year,
            paper_journal_id,
            paper_journal_name,
            paper_journal_volume,
            paper_journal_number,
            paper_no_authors,
            rater_id,
            rater_identifier,
            score,
            time,
        ])
    data_file.seek(0)
    
    response = HttpResponse(data_file, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=data.csv'

    return response
    
    
