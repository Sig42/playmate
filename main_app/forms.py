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

    def clean_url_tesera(self):
        data = self.cleaned_data['url_tesera']
        if data and not data.startswith('https://tesera.ru'):
            raise forms.ValidationError('Ссылка на tesera должна начинаться с "https://tesera.ru/"')
        return data

    def clean_url_bgg(self):
        data = self.cleaned_data['url_bgg']
        if data and not data.startswith('https://tesera.ru'):
            raise forms.ValidationError('Ссылка на boardgamegeeks должна начинаться с "https://boardgamegeek.com/"')
        return data

