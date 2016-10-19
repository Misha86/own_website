from mysite.settings.base import *


try:
    from mysite.settings.local import *
except:
    pass

# noinspection PyBroadException
try:
    from mysite.settings.production import *
except:
    pass