from django.db import models
from django.utils.translation import ugettext_lazy as _
from blog.models import Article
from loginsys.models import Profile


class Comments(models.Model):
    # Translators: This message appears on the home page only
    class Meta:
        db_table = 'comments'
        verbose_name = _("Коментар")
        verbose_name_plural = _("Коментарі")

    comments_create = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата створення"))
    comments_text = models.TextField(verbose_name=_('Текст коментаря'), max_length=200)
    comments_article = models.ForeignKey(Article, related_name="comments", verbose_name=_('Коментар для статті'),
                                         on_delete=models.CASCADE)
    comments_user = models.ForeignKey(Profile, related_name="comments", verbose_name=_("Автор коментаря"))

    def __str__(self):
        return self.comments_text
