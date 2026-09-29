from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
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
    # Variables must be defined in setUp:
    # 1. create_url
    # 2. username
    # 3. password
    # 4. template
    # 5. valid_data
    # 6. model
    # 7. create user to make login
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

    # def test_created_by_is_current_user(self):
    #     self.client.login(
    #         username=self.username,
    #         password=self.password
    #     )
    #     response = self.client.post(self.create_url, data=self.valid_data)
    #     self.assertRedirects(response, self.success_url)
    #     first = self.model.objects.first()
    #     self.assertIsNotNone(first)
    #     self.assertEqual(first.created_by, self.user)


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
    # 3. right_url
    # 4. wrong_url
    def test_uses_correct_template_200(self):
        response = self.client.get(self.right_url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

    def test_context_contains_object(self):
        response = self.client.get(self.right_url)
        self.assertEqual(response.context[self.object_context_name], self.object)

    def test_wrong_pk_gives_404(self):
        response = self.client.get(self.wrong_url)
        self.assertEqual(response.status_code, 404)


class TestListViewMixin:
    # The variables must be defined
    # 1. right_url
    # 2. wrong_url
    # 3. template
    # 4. objects_context_name
    # 5. objects_number
    # 6. first_page_number
    # 7. second_page_number
    # 8. per_page

    def test_view_uses_correct_template_context_name_status(self):
        response = self.client.get(self.right_url)
        self.assertTemplateUsed(response, self.template)
        self.assertIn(self.objects_context_name, response.context)
        self.assertEqual(response.status_code, 200)

    def test_pagination_first_page_has_five_items(self):
        response = self.client.get(self.right_url)
        self.assertEqual(len(response.context[self.objects_context_name]), self.first_page_number)

    def test_pagination_second_page_has_remaining_items(self):
        response = self.client.get(self.right_url, {'page': 2})
        self.assertEqual(len(response.context[self.objects_context_name]), self.second_page_number)

    def test_pagination_invalid_page_returns_404(self):
        response = self.client.get(self.wrong_url)
        self.assertEqual(response.status_code, 404)

    def test_paginate_by_proper_number(self):
        response = self.client.get(self.right_url)
        self.assertEqual(response.context['paginator'].per_page, self.first_page_number)
