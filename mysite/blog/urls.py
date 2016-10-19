# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.views.generic import TemplateView
from blog.views import (start_page,
                        article_list,
                        articles_list_update,
                        article_create,
                        article_update,
                        article_delete,
                        article_detail,
                        add_like,
                        photo)


app_name = 'blog'


urlpatterns = [
    # url(r'^mine/$', MyView.as_view(), name='my-view'),

    # include urls_api
    url(r'^api/', include('blog.class_based.urls')),

    url(r'^$', start_page, name='start_page'),

    url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/list/$', article_list, name='article_list'),
    url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/list/update/$', articles_list_update,
        name='articles_list_update'),
    url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/create/$', article_create, name='article_create'),
    url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/(?P<article_slug>.*)/edit/$', article_update,
        name='article_update'),
    url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/(?P<article_slug>.*)/delete/$', article_delete,
        name='article_delete'),
    url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/(?P<article_slug>.*)/$', article_detail,
        name='article_detail'),
    url(r'^(?P<item_slug>.*)/list/$', photo, name='photo'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact_page.html')),
    url(r'^add_like/(?P<id>[0-9]+)/$', add_like, name='add_like'),
    ]

