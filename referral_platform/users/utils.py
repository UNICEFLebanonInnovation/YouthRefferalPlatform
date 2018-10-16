
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group


def force_default_language(request, language='ar-ar'):
    from django.utils import translation
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language


def get_user_token(user_id):
    try:
        token = Token.objects.get(user_id=user_id)
    except Token.DoesNotExist:
        token = Token.objects.create(user_id=user_id)
    return token.key


def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return True if user and group in user.groups.all() else False
    except Group.DoesNotExist:
        return False
