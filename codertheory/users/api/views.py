from django.contrib.auth import get_user_model
from djoser import utils
from djoser.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response

User = get_user_model()


class TokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to obtain user authentication token.
    """

    serializer_class = settings.SERIALIZERS.token_create
    permission_classes = settings.PERMISSIONS.token_create

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token, context={'request': self.request}).data, status=status.HTTP_200_OK
        )
