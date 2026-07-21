from django.db import models
from django.contrib.auth.models import User


class BoardGame(models.Model):
    title_russian = models.CharField(verbose_name='Название игры на русском',
                                     blank=True,
                                     null=True,
                                     max_length=100)
    title_origin = models.CharField(verbose_name='Название игры на языке оригинала',
                                    blank=True,
                                    null=True,
                                    max_length=100)
    url_tesera = models.URLField(verbose_name='Ссылка на игру на сайте tesera.ru',
                                 blank=True,
                                 null=True,
                                 max_length=200)
    url_bgg = models.URLField(verbose_name='Ссылка на игру на сайте boardgamegeek.com',
                              blank=True,
                              null=True,
                              max_length=100)
    created_by = models.ForeignKey(User,
                                   related_name='created_games',
                                   on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    players= models.ManyToManyField(User,
                                    null=True,
                                    related_name='liked_games')
