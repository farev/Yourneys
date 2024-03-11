from django.forms import ModelForm

from .models import Journey

class JourneyForm(ModelForm):
    class Meta:
        model = Journey
        fields = ('title', 'description', 'topic', 'is_private', 'only_me') 