from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from .models import BoardGame


class BoardGamesView(LoginRequiredMixin, ListView):
    model = BoardGame
    template_name = 'main_app/board_games.html'
    context_object_name = 'board_games'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     title_origin = self.request.GET.get('title')
    #     if look_for:
    #         queryset = queryset.filter(title_origin__contains=title_origin)
    #     return queryset

@login_required
def add_game_to_player(request):
    pass


def home_page(request):
    return render(request, 'base.html', {'data': 'Hello from view!'})


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

