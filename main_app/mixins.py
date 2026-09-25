from asyncio import set_event_loop

from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from Playmate.settings import LOGIN_URL


class AuthorRequiredMixin(LoginRequiredMixin):
    creator_field = 'created_by'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        obj = self.get_object()
        creator = getattr(obj, self.creator_field)
        if creator != request.user:
            raise PermissionDenied(self.permission_denied_message)
        return super().dispatch(request, *args, **kwargs)


class TestCreateViewMixin:
    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(LOGIN_URL, response.url)

    def test_authenticated_user_gets_right_page(self):
        self.client.login(
            username=self.username,
            password=self.password
        )
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertIsInstance(response.context['form'], self.form)

    def test_create_game_success(self):
        self.client.login(
            username=self.username,
            password=self.password
        )
        response = self.client.post(self.create_url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)
        cnt = self.model.objects.count()
        self.assertEqual(cnt, 1)
        first = self.model.objects.first()
        self.assertEqual(first.title, self.valid_data['title'])

    def test_created_by_is_current_user(self):
        self.client.login(
            username=self.username,
            password=self.password
        )
        self.client.post(self.create_url, data=self.valid_data)
        first = self.model.objects.first()
        self.assertIsNotNone(first)
        self.assertEqual(first.created_by, self.user)


class TestDeleteViewMixin:
    # Variables must be defined:
    # 1. right_url
    # 2. model_object -> model of object to delete
    # 3. object -> object to delete
    # 4. author
    # 5. non_author
    # 6. template
    # 7. context_object_name
    # 8. success_url
    # 9. wrong_url

    def test_anonymous_user_redirected(self):
        response = self.client.get(self.right_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(LOGIN_URL, response.url)

    def test_anonymous_user_cannot_delete_game(self):
        response = self.client.post(self.right_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(LOGIN_URL, response.url)
        self.assertTrue(self.model_object.objects.filter(pk=self.object.pk).exists())

    def test_non_author_get_raises_403(self):
        self.client.login(username=self.non_author.username,
                          password=self.password)
        response = self.client.get(self.right_url)
        self.assertEqual(response.status_code, 403)

    def test_non_author_post_raises_403(self):
        self.client.login(username=self.non_author.username,
                          password=self.password)
        response = self.client.post(self.right_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(self.model_object.objects.filter(pk=self.object.pk).exists())

    def test_author_get_returns_200(self):
        self.client.login(username=self.author.username,
                          password=self.password)
        response = self.client.get(self.right_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.template)
        self.assertEqual(response.context[self.context_object_name], self.object)

    def test_author_can_delete_game(self):
        self.client.login(username=self.author.username,
                          password=self.password)
        response = self.client.post(self.right_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)
        self.assertFalse(self.model_object.objects.filter(pk=self.object.pk).exists())

    def test_delete_nonexistent_game_returns_404(self):
        self.client.login(username=self.author.username,
                          password=self.password)
        response = self.client.post(self.wrong_url)
        self.assertEqual(response.status_code, 404)


class TestDetailViewMixin:
    # Variables must be defined:
    # 1. template
    # 2. context_object_name
    # 3. url
    # 4.wrong_url
    def test_uses_correct_template(self):
        response = self.client.get(self.right_url)
        self.assertTemplateUsed(response, self.template)

    def test_context_contains_object(self):
        response = self.client.get(self.right_url)
        self.assertEqual(response.context[self.object_context_name], self.object)

    def test_wrong_pk_gives_404(self):
        response = self.client.get(self.wrong_url)
        self.assertEqual(response.status_code, 404)



# class CommonTestsMixin(TestCase):
# # Variables must be defined in setUp:
#     # right_url
#     # wrong_url
#     # template
#     # user
#     # object
#     # object_model -> model of object to filter and prove exists or not
#     # author
#     # non_author
#
#
#     def test_get_correct_template_200_without_authentication(self):
#         response = self.client.get(self.right_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, self.template)
#
#     def test_get_correct_template_200_with_authentication(self):
#         self.client.login(username=self.user.username,
#                           password=self.user.password)
#         response = self.client.get(self.right_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, self.template)
#
#     def test_context_contains_object(self):
#         response = self.client.get(self.right_url)
#         self.assertEqual(response.context[self.context_object_name], self.object)
#
#     def test_get_wrong_pk_404_without_authentication(self):
#         response = self.client.get(self.wrong_url)
#         self.assertEqual(response.status_code, 404)
#
#     def test_get_wrong_pk_404_with_authentication(self):
#         self.client.login(username=self.user.username,
#                           password=self.user.password)
#         response = self.client.get(wrong_url)
#         self.assertEqual(response.status_code, 404)
#
#     def test_get_anonymous_302(self):
#         response = self.client.get(self.right_url)
#         self.assertEqual(response.status_code, 302)
#         self.assertIn(LOGIN_URL, response.url)
#
#     def test_post_anonymous_302(self):
#         response = self.client.post(self.right_url)
#         self.assertEqual(response.status_code, 302)
#         self.assertIn(LOGIN_URL, response.url)
#
#     def test_anonymous_cannot_delete_object(self):
#         self.client.post(self.right_url)
#         self.assertTrue(self.object_model.objects.filter(pk=self.object.pk).exists())
#
#     def test_get_non_author_403(self):
#         self.client.login(username=self.non_author.username,
#                           password=self.non_author.password)
#         response = self.client.get(self.right_url)
#         self.assertEqual(response.status_code, 403)
#
#     def test_post_non_author_403(self):
#         self.client.login(username=self.non_author.username,
#                           password=self.non_author.password)
#         response = self.client.post(self.right_url)
#         self.assertEqual(response.status_code, 403)
#
#     def test_non_author_cannot_delete_object(self):
#         self.client.login(username=self.non_author.username,
#                           password=self.non_author.password)
#         self.client.post(self.right_url)
#         self.assertTrue(self.object_model.objects.filter(pk=self.object.pk).exists())
#
#     def test_get_author_200(self):
#         self.client.login(username=self.author.username,
#                           password=self.author.password)
#         response = self.client.get(self.right_url)
#         self.assertEqual(response.status_code, 200)
#
