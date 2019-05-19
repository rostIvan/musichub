from drf_yasg import openapi
from rest_framework import serializers

from lessons.serializers import LikeSerializer


class EmptyBody(serializers.Serializer):
    pass


likes_get = {
    'operation_description': "likes",
    'responses': {
        200: openapi.Response(description='',
                              schema=LikeSerializer(many=True))
    },
    'methods': ['GET']
}

likes_post = {
    'operation_description': "likes",
    'request_body': EmptyBody(),
    'responses': {
        200: 'Like lesson or delete like',
        401: 'You can not like something as anonymous user'
    },
    'methods': ['POST']
}
