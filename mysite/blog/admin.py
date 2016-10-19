from django.contrib import admin
from admin.my_admin import misha
from blog.models import Article, Tag
from comment.models import Comments
from django.utils.translation import ugettext_lazy as _


class CommentsInLine(admin.TabularInline):
    model = Comments
    extra = 1
    fk_name = "comments_article"


class ArticleInLine(admin.StackedInline):
    model = Article.article_tag.through
    extra = 1
    verbose_name = _('Стаття тега')
    verbose_name_plural = _("Статті тегу")


class ArticleAdmin(admin.ModelAdmin):

    def uppercase_firstletter_article_text(self):
        return (self.article_text[0]).upper() + self.article_text[1:]
    uppercase_firstletter_article_text.short_description = _("Текст статті")

    fieldsets = [
        (None, {'fields': [('article_title', 'article_slug'), 'article_text', ('article_user', 'article_category',
                                                                               'article_tag'), ]}),
        (_('Зававнтажені картинки'), {
            'classes': ['collapse', ],
            'fields': ['article_image', 'article_likes', ]
        })
    ]
    list_display = ('article_title', uppercase_firstletter_article_text, 'article_date', 'article_user',
                    'article_category', 'article_image', 'id')

    readonly_fields = ['article_likes', ]
    # radio_fields = {'article_user': admin.VERTICAL, }
    # raw_id_fields = ['article_user', ]
    # filter_vertical = ['article_tag', ]
    search_fields = ['article_title']

    # prepopulated_fields = {"article_slug": ("article_title",)}

    list_filter = ['article_category', 'article_date', 'article_user']
    list_per_page = 20
    inlines = [ArticleInLine]

    list_display_links = ['article_title', ]
    list_editable = ['article_category', 'article_user', 'article_image', ]

    list_select_related = ('article_user', )

    # save_as = True

    def get_prepopulated_fields(self, request, obj=None):
        return {"article_slug": ("article_title",)}

    def get_list_filter(self, request):
        list_filter = super(ArticleAdmin, self).get_list_filter(request)
        new_list_filter = ['article_category', 'article_date']
        if request.user.is_superuser:
            return list_filter
        return new_list_filter

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(article_user__user=request.user)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"tag_name": ("tag_title",)}
    inlines = [ArticleInLine]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)

misha.register(Article, ArticleAdmin)        # register in my admin
misha.register(Tag, TagAdmin)                # register in my admin

