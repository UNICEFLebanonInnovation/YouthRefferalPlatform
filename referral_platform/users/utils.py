
def force_default_language(request, language='ar-ar'):
    from django.utils import translation
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language
