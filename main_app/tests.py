from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from Playmate.settings import LOGIN_URL
from .models import BoardGame
from .mixins import TestCreateViewMixin, TestDeleteViewMixin, TestDetailViewMixin
from .forms import BoardGameForm

User = get_user_model()


class BoardGamesViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.games = [
            BoardGame.objects.create(title=f'Игра {i}') for i in range(1, 8)
        ]
        cls.url = reverse('main:games')

    # --- Базовые проверки ---

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main_app/board_games.html')

    def test_view_uses_correct_context_name(self):
        response = self.client.get(self.url)
        self.assertIn('board_games', response.context)

    def test_view_status_code_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_queryset_returns_all_games(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['board_games']), 5)  # первая страница

    # --- Пагинация ---

    def test_pagination_first_page_has_five_items(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['board_games']), 5)

    def test_pagination_second_page_has_remaining_items(self):
        response = self.client.get(self.url, {'page': 2})
        self.assertEqual(len(response.context['board_games']), 2)

    def test_pagination_invalid_page_returns_404(self):
        response = self.client.get(self.url, {'page': 999})
        self.assertEqual(response.status_code, 404)

    def test_paginate_by_is_five(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['paginator'].per_page, 5)

    # --- Фильтрация ---

    def test_filter_by_title_case_insensitive(self):
        response = self.client.get(self.url, {'title': 'игра 1'})
        self.assertEqual(len(response.context['board_games']), 1)
        self.assertEqual(response.context['board_games'][0].title, 'Игра 1')

    def test_filter_by_title_partial_match(self):
        response = self.client.get(self.url, {'title': 'игра'})
        self.assertEqual(response.context['paginator'].count, 7)

    def test_filter_by_title_no_match(self):
        response = self.client.get(self.url, {'title': 'Несуществующая'})
        self.assertEqual(len(response.context['board_games']), 0)

    def test_filter_strips_whitespace(self):
        response = self.client.get(self.url, {'title': '  Игра 1  '})
        self.assertEqual(len(response.context['board_games']), 1)

    def test_filter_empty_string_returns_all(self):
        response = self.client.get(self.url, {'title': ''})
        self.assertEqual(response.context['paginator'].count, 7)

    def test_filter_only_whitespace_returns_all(self):
        response = self.client.get(self.url, {'title': '   '})
        self.assertEqual(response.context['paginator'].count, 7)

    def test_filter_pagination_works_with_filter(self):
        # 7 игр с "Игра", paginate_by=5 -> на 2-й странице 2
        response = self.client.get(self.url, {'title': 'Игра', 'page': 2})
        self.assertEqual(len(response.context['board_games']), 2)


class BoardGameViewTests(TestDetailViewMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.template = 'main_app/board_game.html'
        cls.author = User.objects.create_user(
            username='author', password='1234'
        )
        cls.non_author = User.objects.create_user(
            username='non_author', password='1234'
        )
        cls.object = BoardGame.objects.create(
            title='Catan', created_by=cls.author
        )
        cls.object.players.add(
            cls.author, cls.non_author
        )
        cls.object_context_name = 'game'
        cls.right_url = reverse(
            'main:game', kwargs={'pk': cls.object.pk}
        )
        cls.wrong_url = reverse('main:game', kwargs={'pk': '5555555'})

    # def test_uses_correct_template(self):
    #     response = self.client.get(self.url)
    #     self.assertTemplateUsed(response, self.template)
    #
    # def test_context_contains_game_object(self):
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.context[self.object_context_name], self.game)
    #
    # def test_wrong_pk_gives_404(self):
    #     url = reverse('main:game', kwargs={'pk': 777777})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 404)

    def test_owner_excluded(self):
        self.client.login(username='author',
                          password='1234')
        response = self.client.get(self.right_url)
        players = list(response.context['players'])
        self.assertIn('players', response.context)
        self.assertIn(self.non_author, players)
        self.assertNotIn(self.author, players)


class CreateGameViewTest(TestCreateViewMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model = BoardGame
        cls.username = 'user'
        cls.password = '1234'
        cls.template = 'main_app/board_game_create.html'
        cls.form = BoardGameForm
        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password
        )
        cls.create_url = reverse('main:create_game')
        cls.success_url = reverse('main:games')
        cls.valid_data = {'title': 'Catan',
                          'url_tesera': 'https://tesera.ru/game/catan/'}

    def test_invalid_data_does_not_create_game(self):
        self.client.login(
            username=self.username,
            password=self.password
        )
        response = self.client.post(self.create_url, data={
            'title': '',
            'url_tesera': 'https://somewhere.com',
            'url_bgg': 'https://somewhere.com'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'title', 'Обязательное поле.')
        self.assertFormError(response.context['form'], 'url_tesera',
                             'Ссылка на tesera должна начинаться с "https://tesera.ru/"')
        self.assertFormError(response.context['form'], 'url_bgg',
                             'Ссылка на boardgamegeeks должна начинаться с "https://boardgamegeek.com/"')
        self.assertEqual(BoardGame.objects.count(), 0)


class DeleteGameViewTest(TestDeleteViewMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = '1234'
        cls.author = User.objects.create_user(
            username='author',
            password=cls.password)
        cls.non_author = User.objects.create_user(
            username='non_author',
            password=cls.password)
        cls.model_object = BoardGame
        cls.success_url = reverse('main:games')
        cls.wrong_url = reverse('main:delete_game',
                                  kwargs={'pk': '7777777'})
        cls.context_object_name = 'game'
        cls.template = 'main_app/board_game_delete.html'

    def setUp(self):
        self.object = BoardGame.objects.create(title='Reds',
                                               created_by=self.author)
        self.right_url = reverse('main:delete_game',
                                  kwargs={'pk': self.object.pk})

    def test_delete_only_target_game(self):
        other_game = BoardGame.objects.create(title='Other game',
                                              created_by=self.author)
        self.client.login(username=self.author.username,
                          password=self.password)
        url = reverse('main:delete_game', kwargs={'pk': other_game.pk})
        self.client.post(url)
        self.assertFalse(BoardGame.objects.filter(pk=other_game.pk).exists())
        self.assertTrue(BoardGame.objects.filter(pk=self.object.pk).exists())


class PlayerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.object = User.objects.create_user(username='player',
                                              password='1234')
        cls.right_url = reverse('main:player', kwargs={'pk': cls.object.pk})
        cls.wrong_url = reverse('main:player', kwargs={'pk': '9999999'})
        cls.template = 'main_app/player.html'
        cls.context_object_name = 'player'


