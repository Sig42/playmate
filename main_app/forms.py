from django import forms
from .models import BoardGame

class BoardGameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = ['title',
                  'url_tesera',
                  'url_bgg']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            return title.lower()
        return title

