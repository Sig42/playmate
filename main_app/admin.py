from django.contrib import admin
from .models import (BoardGame, GameAnnouncement, TestAnnouncement, TournamentAnnouncement, SaleAnnouncement,
                     Message)

@admin.register(BoardGame)
class BoarGameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'created_at')
    list_display_links = ('id', 'title')
    list_per_page = 15


@admin.register(GameAnnouncement)
class GameAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'created_by')
    list_per_page = 15


@admin.register(TestAnnouncement)
class TestAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'created_by')
    list_per_page = 15


@admin.register(TournamentAnnouncement)
class TournamentAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'created_by')
    list_per_page = 15

@admin.register(SaleAnnouncement)
class SaleAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'created_by')
    list_per_page = 15


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'created_at')
    list_per_page = 15
