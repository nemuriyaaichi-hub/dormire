from dj_rest_auth.models import TokenModel
from dj_rest_auth.serializers import TokenSerializer
from rest_framework.serializers import SerializerMethodField

from users.serializers import UserSerializer


class TokenSerializer(TokenSerializer):
    user = UserSerializer(read_only=True)
    token = SerializerMethodField()

    class Meta:
        model = TokenModel
        fields = (
            'token',
            'user',
        )

    def get_token(self, object):
        return object.key
