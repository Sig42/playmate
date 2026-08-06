from tabnanny import verbose

from django import forms
from .models import BoardGame, GameAnnouncement


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
        if data and not data.startswith('https://boardgamegeek.com/'):
            raise forms.ValidationError('Ссылка на boardgamegeeks должна начинаться с "https://boardgamegeek.com/"')
        return data


class GameAnnouncementForm(forms.Form):
    game = forms.CharField(label='Название игры',
                           help_text='Попробуйте и на русском и на языке оригинала. '
                                     'Можно ввести только часть названия игры.',
                           max_length=100,
                           strip=True,
                           required=False)
    city = forms.CharField(label='Город',
                           help_text='Можно ввести только часть названия города.',
                           max_length=100,
                           strip=True,
                           required=False)
    place = forms.CharField(label='Место',
                           help_text='Название заведения, в котором проходит игра',
                           max_length=100,
                           strip=True,
                           required=False)
    date = forms.DateField(label='Дата проведения',
                           required=False,
                           widget=forms.DateInput(attrs={'type': 'date'}))
    is_online = forms.BooleanField(label='Искать онлайн игры',
                                   required=False)
