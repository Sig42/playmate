from django.contrib import admin
from .models import BoardGame, GameAnnouncement, TestAnnouncement, TournamentAnnouncement, SaleAnnouncement, Message

admin.site.register(BoardGame)
admin.site.register(GameAnnouncement)
admin.site.register(TestAnnouncement)
admin.site.register(TournamentAnnouncement)
admin.site.register(SaleAnnouncement)
admin.site.register(Message)
