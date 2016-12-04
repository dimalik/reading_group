import json
import base64
from StringIO import StringIO

from django.views.generic import TemplateView
from django.http import HttpResponse

# from ggplot import *
# from PIL import Image
# import pandas

class HomeView(TemplateView):
    template_name = 'index.html'
