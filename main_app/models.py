from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class BoardGame(models.Model):
    title = models.CharField(verbose_name='Название игры',
                             blank=False,
                             null=False,
                             max_length=100)
    url_tesera = models.URLField(verbose_name='Ссылка на игру на сайте tesera.ru',
                                 blank=True,
                                 null=True,
                                 max_length=200)
    url_bgg = models.URLField(verbose_name='Ссылка на игру на сайте boardgamegeek.com',
                              blank=True,
                              null=True,
                              max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   related_name='created_games',
                                   on_delete=models.SET_NULL,
                                   null=True)
    players= models.ManyToManyField(User,
                                    related_name='liked_games',
                                    null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:game', kwargs={'pk': self.pk})

    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]
        ordering = ['title']
        verbose_name = 'Настолка'
        verbose_name_plural = 'Настолки'


class Announcement(models.Model):
    city = models.CharField(verbose_name='Город',
                            help_text='Если игра будет онлайн укажите площадку, например: Tabletop',
                            max_length=100,
                            blank = True,
                            null = True,
                            db_index=True)
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
                                help_text='Формат ГГГГ-ММ-ДД ЧЧ:ММ',
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

    def __str__(self):
        return f'GameAnnouncement pk-{self.pk}'

    class Meta:
        verbose_name = "Анонс игры"
        verbose_name_plural = "Анонсы игр"
        ordering = ['-date']


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

    def __str__(self):
        return f'TestAnnouncement pk-{self.pk}'

    class Meta:
        verbose_name = "Анонс тестирования игр"
        verbose_name_plural = "Анонсы тестирования игр"
        ordering = ['-date']


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

    def __str__(self):
        return f'TournamentAnnouncement pk-{self.pk}'

    class Meta:
        verbose_name = "Анонс турнира"
        verbose_name_plural = "Анонсы турниров"
        ordering = ['-date']


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

    def __str__(self):
        return f'SaleAnnouncement pk-{self.pk}'

    class Meta:
        verbose_name = "Объявление о продаже"
        verbose_name_plural = "Объявления о продаже"
        ordering = ['-created_at']