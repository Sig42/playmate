from django import forms
from .models import BoardGame

class BoardGameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = ['title_russian',
                  'title_origin',
                  'url_tesera',
                  'url_bgg']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    def save(self, user=None, commit=True):
        instance = super().save(commit=False)
        if user and user.is_authenticated:
            instance.created_by = user
        if commit:
            instance.save()
            self.save_m2m()
        return instance
