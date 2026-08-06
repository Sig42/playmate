from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import BoardGame, GameAnnouncement, TestAnnouncement, TournamentAnnouncement, SaleAnnouncement
from .forms import BoardGameForm, GameAnnouncementForm

# Проверить все вьюхи и шаблоны на наличие запросов N+1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class PlayersView(ListView):
    model = get_user_model()
    template_name = 'main_app/players.html'
    context_object_name = 'players'

    def get_queryset(self):
        user = get_user_model()
        queryset = user.objects.prefetch_related('liked_games').all()
        return queryset


class BoardGamesView(ListView):
    model = BoardGame
    template_name = 'main_app/board_games.html'
    context_object_name = 'board_games'

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title.lower())
        return queryset


class BoardGameView(DetailView):
    model = BoardGame
    template_name = 'main_app/board_game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = BoardGame.objects.get(pk=self.object.pk)
        context['game'] = game
        context['players'] = game.players.all()
        return context


class CreateGameView(LoginRequiredMixin, CreateView):
    model = BoardGame
    form_class = BoardGameForm
    template_name = 'main_app/board_game_create.html'
    login_url = 'accounts/signup'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DeleteGameView(LoginRequiredMixin, DeleteView):
    model = BoardGame
    template_name = 'main_app/board_game_delete.html'
    login_url = 'accounts:signup'
    success_url = reverse_lazy('main:games')


class PlayerView(DetailView):
    model = get_user_model()
    template_name = 'main_app/player.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = self.object.liked_games.all()
        return context


class GameAnnouncementsView(ListView):
    model = GameAnnouncement
    template_name = 'main_app/game_announcements.html'
    context_object_name = 'game_announcements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GameAnnouncementForm()
        return context

    def get_queryset(self):
        queryset = GameAnnouncement.objects.select_related('boardgame').all()
        game = self.request.GET.get('game')
        city = self.request.GET.get('city')
        place = self.request.GET.get('place')
        date = self.request.GET.get('date')
        is_online = self.request.GET.get('is_online')

        if game:
            queryset = queryset.filter(boardgame__title__icontains=game.lower())
        if city:
            queryset = queryset.filter(city__icontains=city.lower())
        if place:
            queryset = queryset.filter(place__icontains=place.lower())
        if date:
            queryset = queryset.filter(date__date=date)
        if is_online:
            queryset = queryset.filter(is_online=True)
        return queryset


class TestAnnouncementsView(ListView):
    model = TestAnnouncement
    template_name = 'main_app/test_announcements.html'
    context_object_name = 'test_announcements'


class TournamentAnnouncementsView(ListView):
    model = TournamentAnnouncement
    template_name = 'main_app/tournament_announcements.html'
    context_object_name = 'tournament_announcements'


class SaleAnnouncementsView(ListView):
    model = SaleAnnouncement
    template_name = 'main_app/sale_announcements.html'
    context_object_name = 'sale_announcements'


def home_page(request):
    return render(request, 'base.html', {'data': 'Hello from view!'})


# Function to add a game to liked_games field of User model
def add_liked_game(request, pk):
    user = request.user
    user.liked_games.add(pk)
    return render(request, 'main_app/liked_game_added.html')
