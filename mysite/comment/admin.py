from django.contrib import admin
from comment.models import Comments
from django.utils.translation import ugettext_lazy as _


class CommentAdmin(admin.ModelAdmin):
    def shot_comments_text(self):
        num_letters = len(self.comments_text)
        if num_letters > 75:
            return self.comments_text[:75] + '...'
        return self.comments_text
    shot_comments_text.short_description = _("Текст коментаря")

    list_display = ['comments_article', 'comments_create', shot_comments_text, 'comments_user']
    search_fields = ['comments_text', 'comments_article']
    # radio_fields = {'comments_article': admin.VERTICAL}
    # raw_id_fields = ['comments_article', ]
    list_per_page = 20


admin.site.register(Comments, CommentAdmin)