from django import forms
from .models import BoardGame, TournamentAnnouncement, SaleAnnouncement


class BoardGameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = ['title',
                  'url_tesera',
                  'url_bgg']

    url_tesera = forms.URLField(label='Ссылка на tesera.ru',
                                help_text='Поле не является обязательным',
                                required=False)
    url_bgg = forms.URLField(label='Ссылка на boardgamegeek.com',
                             help_text='Поле не является обязательным',
                             required=False)

    def clean_url_tesera(self):
        data = self.cleaned_data['url_tesera']
        if data and not data.startswith('https://tesera.ru'):
            raise forms.ValidationError('Ссылка на tesera должна начинаться с "https://tesera.ru/"')
        return data

    def clean_url_bgg(self):
        data = self.cleaned_data['url_bgg']
        if data and not data.startswith('https://boardgamegeek.com/'):
            raise forms.ValidationError('Ссылка на boardgamegeek должна начинаться с "https://boardgamegeek.com/"')
        return data


class GameAnnouncementsFilterForm(forms.Form):
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


class TestAnnouncementsFilterForm(forms.Form):
    title = forms.CharField(label='Название игры',
                            help_text='Можно ввести только часть названия игры',
                            max_length=100,
                            strip=True,
                            required=False)

    city = forms.CharField(label='Город',
                           help_text='Можно ввести только часть названия города',
                           max_length=100,
                           strip=True,
                           required=False)

    date = forms.DateField(label='Дата проведения',
                           required=False,
                           widget=forms.DateInput(attrs={'type': 'date'}))

    is_online = forms.BooleanField(label='Будет проходить онлайн',
                                   required=False)


class TournamentAnnouncementForm(forms.ModelForm):
    class Meta:
        model = TournamentAnnouncement
        fields = ['boardgame',
                  'city',
                  'address',
                  'date',
                  'is_online',
                  'conditions',
                  'contact']


class TournamentAnnouncementFilterForm(forms.Form):
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
    date = forms.DateField(label='Дата проведения',
                           required=False,
                           widget=forms.DateInput(attrs={'type': 'date'}))
    is_online = forms.BooleanField(label='Искать онлайн игры',
                                   required=False)


class SaleAnnouncementForm(forms.ModelForm):
    class Meta:
        model = SaleAnnouncement
        fields =['boardgame',
                 'price',
                 'description',
                 'city',
                 'contact']


class SaleAnnouncementFilterForm(forms.Form):
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
