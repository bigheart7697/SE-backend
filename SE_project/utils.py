from apps.accounts.serializers import UserSerializer
# from SE_project.apps.accounts.serializers import UserSerializer


def custom_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }