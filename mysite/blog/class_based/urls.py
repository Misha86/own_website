from django.conf.urls import url, include
from blog.class_based.views import ArticleList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete

app_name = 'api'

urlpatterns = [
    url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/create/$', ArticleCreate.as_view(), name='article_create'),
    url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/(?P<article_slug>.*)/edit/$', ArticleUpdate.as_view(),
        name='article_update'),
    url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/(?P<article_slug>.*)/delete/$', ArticleDelete.as_view(),
        name='article_delete'),
    url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/list/$', ArticleList.as_view(), name='article_list'),
    url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/(?P<article_slug>.*)/$', ArticleDetail.as_view(),
        name='article_detail'),





    # url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/(?P<article_slug>.*)/delete/$', 'blog.views.article_delete',
    #     name='article_delete'),
    # url(r'^(?P<item_slug>.*)/(?P<category_slug>.*)/(?P<article_slug>.*)/$', 'blog.views.article_detail',
    #     name='article_detail')
]

