from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class AuthorRequiredMixin(LoginRequiredMixin):
    creator_field = 'created_by'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        obj = self.get_object()
        creator = getattr(obj, self.creator_field)
        if creator != request.user:
            raise PermissionDenied(self.permission_denied_message)
        return response
