from django.forms import ModelForm
from suggestions.models import Suggestion

class SuggestionCreateForm(ModelForm):
    class Meta:
        model = Suggestion
        exclude = ('uploader',)
