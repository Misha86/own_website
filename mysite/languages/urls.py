from django.conf.urls import url
from languages.views import set_language


urlpatterns = [
    url(r'^(?P<lang_code>.*)/$', set_language, name='set_language'),
    ]

