from django.urls import path
from .views import BoardGamesView

urlpatterns = [
    path('games/', BoardGamesView.as_view(), name='games'),

]