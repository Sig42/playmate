# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from .models import BoardGame, GameAnnouncement, TestAnnouncement, TournamentAnnouncement, SaleAnnouncement


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


class GameAnnouncementsView(ListView):
    model = GameAnnouncement
    template_name = 'main_app/game_announcements.html'
    context_object_name = 'game_announcements'


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



# @login_required
# def create_game(request):
#     if request.method == 'POST':
#         form = GameForm(request.POST)
#         if form.is_valid():
#             game = form.save(user=request.user)  # Передаем пользователя
#             return redirect('game_detail', pk=game.pk)
#     else:
#         form = GameForm()
#     return render(request, 'create_game.html', {'form': form})

