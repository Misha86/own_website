from __future__ import unicode_literals
from functools import wraps
from django import template
from django.utils.encoding import force_text
from django.utils.safestring import SafeData, mark_safe


register = template.Library()

#######################
# STRING DECORATOR    #
#######################


def stringfilter(func):
    """
    Decorator for filters which should only receive unicode objects. The object
    passed as the first positional argument will be converted to a unicode
    object.
    """
    def _dec(*args, **kwargs):
        if args:
            args = list(args)
            args[0] = force_text(args[0])
            if (isinstance(args[0], SafeData) and
                    getattr(_dec._decorated_function, 'is_safe', False)):
                return mark_safe(func(*args, **kwargs))
        return func(*args, **kwargs)

    # Include a reference to the real function (used to check original
    # arguments by the template parser, and to bear the 'is_safe' attribute
    # when multiple decorators are applied).
    _dec._decorated_function = getattr(func, '_decorated_function', func)

    return wraps(func)(_dec)


###################
# STRINGS         #
###################


@register.filter(is_safe=True)
@stringfilter
def my(value, arg):
    """ Удаляет вcе вхождения arg из данной строки """
    val = ''
    for v in value:
        if arg == ' ':
            v = v + arg
            val += v
        else:
            if v == ' ':
                v = v
            else:
                v = v + arg
            val += v
    return val

@register.filter(is_safe=True)
@stringfilter
def shot_text(value, arg):
    """ Робить текст коротше до відповідної кількості символів """
    arg = int(arg)
    if len(value) > arg:
        shot_text = value[:arg] + '...'
        return shot_text
    else:
        return value


