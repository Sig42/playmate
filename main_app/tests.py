from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import BoardGame, GameAnnouncement
from .mixins import TestCreateViewMixin, TestDeleteViewMixin, TestDetailViewMixin, TestListViewMixin
from .forms import BoardGameForm, GameAnnouncementsFilterForm

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
        self.assertEqual(len(response.context['board_games']), 5)

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
        self.assertEqual(response.context['paginator'].count, 1)
        self.assertEqual(response.context['board_games'][0].title, 'Игра 1')

    def test_filter_by_title_partial_match(self):
        response = self.client.get(self.url, {'title': 'игра'})
        self.assertEqual(response.context['paginator'].count, 7)

    def test_filter_by_title_no_match(self):
        response = self.client.get(self.url, {'title': 'Несуществующая'})
        self.assertEqual(response.context['paginator'].count, 0)

    def test_filter_strips_whitespace(self):
        response = self.client.get(self.url, {'title': '  Игра 1  '})
        self.assertEqual(response.context['paginator'].count, 1)

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


class PlayerViewTest(TestDetailViewMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.object = User.objects.create_user(username='player',
                                              password='1234')
        cls.right_url = reverse('main:player', kwargs={'pk': cls.object.pk})
        cls.wrong_url = reverse('main:player', kwargs={'pk': '9999999'})
        cls.template = 'main_app/player.html'
        cls.object_context_name = 'player'
        cls.game_1 = BoardGame.objects.create(title='game_1')
        cls.game_2 = BoardGame.objects.create(title='game_2')
        cls.object.liked_games.add(cls.game_1, cls.game_2)

    def test_context_contains_right_info(self):
        response = self.client.get(self.right_url)
        self.assertEqual(response.context['pk'], self.object.pk)
        self.assertEqual(list(response.context['games']), list(self.object.liked_games.all()))


class GameAnnouncementsViewTest(TestListViewMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.right_url = reverse('main:game_anns')
        cls.wrong_url = reverse('main:game_anns') + '?page=777'
        cls.template = 'main_app/game_announcements.html'
        cls.objects_context_name = 'game_announcements'
        cls.objects_number = 7
        cls.first_page_number = 5
        cls.second_page_number = 2
        cls.user = User.objects.create_user(
            username='user',
            password='1234'
        )
        cls.boardgame1 = BoardGame.objects.create(title='Манчкин')
        cls.boardgame2 = BoardGame.objects.create(title='Каркассон')
        cls.announcements = []
        for i in range(7):
            announcement = GameAnnouncement.objects.create(
                boardgame=cls.boardgame1 if i % 2 == 0 else cls.boardgame2,
                created_by=cls.user,
                city='Москва' if i < 4 else 'Санкт-Петербург',
                place=f'Место {i}',
                date=timezone.now() + timedelta(days=i),
                is_online=(i % 2 == 0),
            )
            cls.announcements.append(announcement)

    def test_filter_form_in_context(self):
        response = self.client.get(self.right_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], GameAnnouncementsFilterForm)

    def test_pagination_first_page(self):
        response = self.client.get(self.right_url)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['game_announcements']), self.first_page_number)

    def test_pagination_second_page(self):
        response = self.client.get(self.right_url, {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['game_announcements']), self.second_page_number)

    def test_filter_by_game(self):
        response = self.client.get(self.right_url, {'game': 'Манчкин'})
        announcements = response.context['game_announcements']
        self.assertTrue(len(announcements) == 4)
        for a in announcements:
            self.assertIn('манчкин', a.boardgame.title.lower())

    def test_filter_by_game_partial_match(self):
        response = self.client.get(self.right_url, {'game': 'каркас'})
        announcements = response.context['game_announcements']
        self.assertTrue(len(announcements) == 3)
        for a in announcements:
            self.assertIn('каркас', a.boardgame.title.lower())

    def test_filter_by_city(self):
        response = self.client.get(self.right_url, {'city': 'Москва'})
        announcements = response.context['game_announcements']
        self.assertTrue(len(announcements) == 4)
        for a in announcements:
            self.assertIn('москва', a.city.lower())

    def test_filter_by_place(self):
        response = self.client.get(self.right_url, {'place': 'Место 1'})
        announcements = response.context['game_announcements']
        self.assertEqual(len(announcements), 1)
        self.assertIn('место 1', announcements[0].place.lower())

    def test_filter_by_date(self):
        target = self.announcements[2]
        target_date = target.date.date()
        response = self.client.get(self.right_url, {'date': target_date})
        announcements = response.context['game_announcements']
        self.assertEqual(len(announcements), 1)
        self.assertEqual(announcements[0].pk, target.pk)

    def test_filter_by_is_online(self):
        response = self.client.get(self.right_url, {'is_online': 'true'})
        announcements = response.context['game_announcements']
        self.assertTrue(len(announcements) == 4)
        for a in announcements:
            self.assertTrue(a.is_online)

    def test_combined_filters(self):
        response = self.client.get(self.right_url, {
            'city': 'Москва',
            'is_online': 'true',
        })
        announcements = response.context['game_announcements']
        self.assertTrue(len(announcements) == 2)
        for a in announcements:
            self.assertIn('москва', a.city.lower())
            self.assertTrue(a.is_online)

    def test_empty_filters_returns_all(self):
        response = self.client.get(self.right_url)
        total = GameAnnouncement.objects.count()
        self.assertEqual(response.context['paginator'].count, total)

    def test_filter_with_no_results(self):
        response = self.client.get(self.right_url, {'game': 'НесуществующаяИгра123'})
        self.assertEqual(len(response.context['game_announcements']), 0)

    def test_select_related_used(self):
        with self.assertNumQueries(2):
            self.client.get(self.right_url)
