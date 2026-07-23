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
                                   on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    players= models.ManyToManyField(User,
                                    null=True,
                                    related_name='liked_games')

    class Meta:
        indexes = [
            models.Index(fields=['title_russian']),
            models.Index(fields=['title_origin'])
        ]
        verbose_name = 'Настолка'
        verbose_name_plural = 'Настолки'


class Announcement(models.Model):
    city = models.CharField(verbose_name='Город',
                            help_text='Если игра будет онлайн укажите площадку, например: Tabletop',
                            max_length=100,
                            blank = True,
                            null = True)
    address = models.CharField(verbose_name='Адрес мероприятия',
                               help_text='Пропустите это поле, если игра будет онлайн',
                               max_length=200,
                               blank=True,
                               null=True)
    is_online = models.BooleanField(verbose_name='Онлайн мероприятие',
                                    help_text='Поставьте галочку, если игра будет онлайн',
                                    default=False)
    contact = models.CharField(verbose_name='Контакты',
                               help_text='Укажите контакты для связи',
                               max_length=200,
                               blank=True,
                               null=True)
    date = models.DateTimeField(verbose_name='Дата и время проведения мероприятия',
                                help_text='Сообщение автоматически удалится через неделю с указанной даты',
                                blank=False,
                                null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class GameAnnouncement(Announcement):
    boardgame = models.ForeignKey(BoardGame,
                                  verbose_name='Настолка',
                                  help_text='Если в выборе нет нужной игры - создайте ее, пожалуйста ("Игры" в '
                                            'главном меню). Эту Вселенную делаете Вы ))',
                                  on_delete=models.CASCADE,
                                  blank=False,
                                  null=False)
    place = models.CharField(verbose_name='Название заведения, где будет проводиться игра',
                             help_text='Если игра будет проводиться дома - напишите "домашняя игра"',
                             blank=False,
                             null=False,
                             max_length=100)
    conditions = models.TextField(verbose_name='Стоимость и другие условия',
                                  blank=False,
                                  null=False)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name='game_ann',
                                   null=False)


class TestAnnouncement(Announcement):
    title = models.CharField(verbose_name='Название будущей игры',
                             blank=True,
                             null=True,
                             max_length=100)
    description = models.TextField(verbose_name='Краткое описание игры, механик',
                                   blank=False,
                                   null=False)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   related_name='test_ann')
    conditions = models.TextField(verbose_name='Прочая информация о мероприятии')


class TournamentAnnouncement(Announcement):
    boardgame = models.ForeignKey(BoardGame,
                                  verbose_name='Настолка',
                                  help_text='Если в выборе нет нужной игры - создайте ее, пожалуйста ("Игры" в '
                                            'главном меню). Эту Вселенную делаете Вы ))',
                                  on_delete=models.CASCADE,
                                  blank=False,
                                  null=False)
    conditions = models.TextField(verbose_name='Условия проведения турнира',
                                  blank=False,
                                  null=False)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   related_name='tour_ann')


class SaleAnnouncement(models.Model):
    boardgame = models.ForeignKey(BoardGame,
                                  verbose_name='Настолка',
                                  help_text='Если в выборе нет нужной игры - создайте ее, пожалуйста ("Игры" в '
                                            'главном меню). Эту Вселенную делаете Вы ))',
                                  on_delete=models.CASCADE,
                                  blank=False,
                                  null=False)
    price = models.DecimalField(verbose_name='Цена',
                                max_digits=8,
                                decimal_places=2,
                                blank=False,
                                null=False)
    description = models.TextField(verbose_name='Описание, состояние и прочее',
                                   blank=False,
                                   null=False)
    city = models.CharField(verbose_name='Укажите Ваш город',
                            max_length=100,
                            blank=True,
                            null=True)
    contact = models.CharField(verbose_name='Контакты',
                               help_text='Укажите контакты для связи',
                               max_length=200,
                               blank=True,
                               null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   related_name='sale_ann')
