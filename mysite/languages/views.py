from django.shortcuts import redirect
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, check_for_language, get_language, to_locale,)


def set_language(request, lang_code):

        path = request.META.get('HTTP_REFERER', '/')
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
                return redirect(path)
        # user_language = lang_code
        # translation.activate(user_language)
        # request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        # return redirect(path)

