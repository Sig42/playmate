from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import (BoardGame, GameAnnouncement, TestAnnouncement, TournamentAnnouncement, SaleAnnouncement,
                     Message)
from .forms import (BoardGameForm, GameAnnouncementsFilterForm, TestAnnouncementsFilterForm,
                    TournamentAnnouncementFilterForm, TournamentAnnouncementForm, SaleAnnouncementFilterForm,
                    SaleAnnouncementForm)


# Проверить все вьюхи и шаблоны на наличие запросов N+1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class PlayersView(ListView):
    model = User
    template_name = 'main_app/players.html'
    context_object_name = 'players'

    def get_queryset(self):
        queryset = User.objects.prefetch_related('liked_games').all()
        return queryset


class BoardGamesView(ListView):
    model = BoardGame
    template_name = 'main_app/board_games.html'
    context_object_name = 'board_games'

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        if title:
            title = title.strip().lower()
            queryset = queryset.filter(title__icontains=title)
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
    form_class = BoardGameForm
    template_name = 'main_app/board_game_create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DeleteGameView(LoginRequiredMixin, DeleteView):
    model = BoardGame
    template_name = 'main_app/board_game_delete.html'
    success_url = reverse_lazy('main:games')


class PlayerView(DetailView):
    model = User
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
        context['form'] = GameAnnouncementsFilterForm()
        return context

    def get_queryset(self):
        queryset = GameAnnouncement.objects.select_related('boardgame', 'created_by').all()
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


class CreateGameAnnouncementView(LoginRequiredMixin, CreateView):
    model = GameAnnouncement
    fields = ['boardgame',
              'city',
              'address',
              'place',
              'date',
              'is_online',
              'contact',
              'conditions']
    template_name = 'main_app/game_announcement_create.html'
    success_url = reverse_lazy('main:game_anns')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DeleteGameAnnouncement(LoginRequiredMixin, DeleteView):
    model = GameAnnouncement
    template_name = 'main_app/game_announcement_delete.html'
    success_url = reverse_lazy('main:game_anns')


class TestAnnouncementsView(ListView):
    model = TestAnnouncement
    template_name = 'main_app/test_announcements.html'
    context_object_name = 'test_announcements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TestAnnouncementsFilterForm()
        return context

    def get_queryset(self):
        queryset = TestAnnouncement.objects.select_related('created_by').all()
        title = self.request.GET.get('title')
        city = self.request.GET.get('city')
        date = self.request.GET.get('date')
        is_online = self.request.GET.get('is_online')

        if title:
            title = title.lower()
            queryset = queryset.filter(title__icontains=title)
        if city:
            city = city
            queryset = queryset.filter(city__icontains=city)
        if date:
            queryset = queryset.filter(date__date=date)
        if is_online:
            queryset = queryset.filter(is_online=True)
        return queryset


class CreateTestAnnouncementView(LoginRequiredMixin, CreateView):
    model = TestAnnouncement
    fields = ['title',
              'description',
              'city',
              'address',
              'date',
              'is_online',
              'conditions',
              'contact']
    template_name = 'main_app/test_announcement_create.html'
    success_url = reverse_lazy('main:test_anns')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DeleteTestAnnouncementView(LoginRequiredMixin, DeleteView):
    model = TestAnnouncement
    template_name = 'main_app/test_announcement_delete.html'
    success_url = reverse_lazy('main:test_anns')


class TournamentAnnouncementsView(ListView):
    model = TournamentAnnouncement
    template_name = 'main_app/tournament_announcements.html'
    context_object_name = 'tournament_announcements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TournamentAnnouncementFilterForm()
        return context


    def get_queryset(self):
        queryset = TournamentAnnouncement.objects.select_related('boardgame', 'created_by').all()
        game = self.request.GET.get('game')
        city = self.request.GET.get('city')
        date = self.request.GET.get('date')
        is_online = self.request.GET.get('is_online')

        if game:
            queryset = queryset.filter(boardgame__title__icontains=game.lower())
        if city:
            queryset = queryset.filter(city__icontains=city.lower())
        if date:
            queryset = queryset.filter(date__date=date)
        if is_online:
            queryset = queryset.filter(is_online=True)
        return queryset


class TournamentAnnouncementCreateView(LoginRequiredMixin, CreateView):
    form_class = TournamentAnnouncementForm
    template_name = 'main_app/tournament_announcement_create.html'
    success_url = reverse_lazy('main:tournament_anns')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TournamentAnnouncementDeleteView(LoginRequiredMixin, DeleteView):
    model = TournamentAnnouncement
    template_name = 'main_app/tournament_announcement_delete.html'
    success_url = reverse_lazy('main:tournament_anns')


class SaleAnnouncementsView(ListView):
    model = SaleAnnouncement
    template_name = 'main_app/sale_announcements.html'
    context_object_name = 'sale_announcements'

    def get_queryset(self):
        queryset = SaleAnnouncement.objects.select_related('boardgame', 'created_by').all()
        game = self.request.GET.get('game')
        city = self.request.GET.get('city')
        if game:
            queryset = queryset.filter(boardgame__title__icontains=game.lower())
        if city:
            queryset = queryset.filter(city__contains=city.lower())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SaleAnnouncementFilterForm()
        return context


class SaleAnnouncementCreateView(LoginRequiredMixin, CreateView):
    form_class = SaleAnnouncementForm
    template_name = 'main_app/sale_announcement_create.html'
    success_url = reverse_lazy('main:sale_anns')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SaleAnnouncementDeleteView(LoginRequiredMixin, DeleteView):
    model = SaleAnnouncement
    template_name = 'main_app/sale_announcement_delete.html'
    success_url = reverse_lazy('main:sale_anns')


class PlaymatesListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'main_app/playmates.html'
    context_object_name = 'playmates'

    def get_queryset(self):
        queryset = User.objects.filter(Q(sent_messages__to_user=self.request.user)
                                       | Q(received_messages__from_user=self.request.user)).distinct()
        return queryset


"""
class MessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'main_app/messages.html'
    context_object_name = 'messages'

    def get_queryset(self):
        playmate_id = self.kwargs.get('pk')
        queryset = Message.mngr.get_my_msgs(user=self.request.user).filter(Q(from_user__pk=playmate_id) |
                                                                           Q(to_user__pk=playmate_id))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playmate_name'] = get_object_or_404(User, pk=self.kwargs.get('pk')).username
        return context

"""


class MessageCreateView(CreateView):
    model = Message
    fields = ['text']
    template_name = 'main_app/messages.html'

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        if pk:
            return reverse_lazy('main:messages', kwargs={'pk': pk})
        return reverse_lazy('main:playmates')

    def form_valid(self, form):
        form.instance.from_user = self.request.user
        form.instance.to_user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playmate_id = self.kwargs.get('pk')
        user = self.request.user
        message_filters = (Q(from_user__pk=playmate_id) | Q(to_user__pk=playmate_id))
        context['messages'] = Message.mngr.get_my_msgs(user=user).filter(message_filters)
        return context


def home_page(request):
    return render(request, 'base.html')


# Function to add a game to liked_games field of User model
@login_required
def add_liked_game(request, pk):
    user = request.user
    user.liked_games.add(pk)
    return render(request, 'main_app/liked_game_added.html')
