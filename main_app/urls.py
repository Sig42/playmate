from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('games/', views.BoardGamesView.as_view(), name='games'),
    path('game/<int:pk>/', views.BoardGameView.as_view(), name='game'),
    path('game/create/', views.CreateGameView.as_view(), name='create_game'),
    path('game/<int:pk>/delete/', views.DeleteGameView.as_view(), name='delete_game'),
    path('add_liked_game/<int:pk>/', views.add_liked_game, name='add_liked_game'),
    path('game_announcements/', views.GameAnnouncementsView.as_view(), name='game_anns'),
    path('test_announcements/', views.TestAnnouncementsView.as_view(), name='test_anns'),
    path('tournament_announcements/', views.TournamentAnnouncementsView.as_view(), name='tournament_anns'),
    path('sale_announcements/', views.SaleAnnouncementsView.as_view(), name='sale_anns'),
    path('players/', views.PlayersView.as_view(), name='players'),
    path('player/<int:pk>/', views.PlayerView.as_view(), name='player'),
]
