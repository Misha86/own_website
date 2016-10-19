from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from loginsys.models import Profile
from navigation.models import Category
from django.utils.translation import ugettext_lazy as _
import os


def upload_location(instance, filename):
    path = 'upload/article_images'
    if instance.id is not None:
        return os.path.join(path, str(instance.id), str(filename))
    article = Article.objects.order_by("id").last()
    if not article:
        return os.path.join(path, 'FIRST_article', str(filename))
    if article.id is not None:
        new_id = article.id + 1
        return os.path.join(path, str(new_id), str(filename))


class Tag(models.Model):
    tag_title = models.CharField(max_length=50, verbose_name=_('Назва тега'))
    tag_name = models.SlugField(verbose_name=_('Ім`я тега транслітом'))

    class Meta:
        db_table = "tags"
        verbose_name = _("Тег")
        verbose_name_plural = _("Тегі")

    def __str__(self):
        return self.tag_title


class ArticleManager(models.Manager):
    def get_by_natural_key(self, article_title):
        return self.get(article_title=article_title)


class Article(models.Model):
    objects = ArticleManager()

    article_user = models.ForeignKey(Profile, related_name="articles", verbose_name=_("Автор статті"))
    article_title = models.CharField(max_length=50, verbose_name=_("Назва статті"), unique=True)
    article_text = models.TextField(max_length=1000, verbose_name=_("Текст статті"))
    article_category = models.ForeignKey(Category, related_name="articles", verbose_name=_("Категорія"),
                                         on_delete=models.CASCADE)
    article_tag = models.ManyToManyField(Tag, related_name="articles", verbose_name=_("Тегі"))
    article_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата створення"))
    article_update = models.DateTimeField(auto_now=True, verbose_name=_("Дата оновлення"))
    article_likes = models.IntegerField(verbose_name=_("Подобається"), default=0)
    article_image = models.ImageField(verbose_name=_("Картинки"), upload_to=upload_location, blank=True, null=True,
                                      help_text=_("Зображення до статті"))
    article_slug = models.SlugField(verbose_name=_("Ім`я статті транслітом"), blank=True, unique=True)

    class Meta:
        db_table = "articles"
        verbose_name = _("Стаття")
        verbose_name_plural = _("Статті")

    def __str__(self):
        return self.article_title

    def natural_key(self):
        return self.article_title

    def get_image(self):
        if not self.article_image:
            return False
        else:
            return True

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'item_slug': self.article_category.menu_category.menu_name,
                                                      'category_slug': self.article_category.category_name,
                                                      'article_slug': self.article_slug})
    get_absolute_url.admin_order_field = 'article_date'
    get_absolute_url.short_description = _('Абсолютна адреса')


