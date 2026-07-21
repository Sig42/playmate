from django import forms
from .models import BoardGame

class BoardGameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = ['title_russian',
                  'title_origin',
                  'url_tesera',
                  'url_bgg']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user and user.is_authenticated:
            instance.created_by = user
        if commit:
            instance.save()
            self.save_m2m()
        return instance
