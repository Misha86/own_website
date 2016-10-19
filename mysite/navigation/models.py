from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class MenuItem(models.Model):
    class Meta:
        db_table = "menu_items"
        verbose_name = _("Пункт меню")
        verbose_name_plural = _("Пункти меню")

    menu_title = models.CharField(max_length=50, verbose_name=_('Назва пункту меню'))
    menu_name = models.SlugField(verbose_name=_('Ім`я пункту меню транслітом'))
    menu_number = models.IntegerField(verbose_name=_('Номер пункту меню'), default=1)
    menu_url = models.CharField(max_length=200, verbose_name=_('Адреса для виконання'), blank=True)
    menu_type = models.CharField(max_length=50, choices=(('single', _('звичайний')),
                                                         ('single active', _('звичайний активний')),
                                                         ('dropdown', _('випадаючий'))),
                                 verbose_name=_('Тип пункту меню'))

    def __str__(self):
        return self.menu_title


class Category(models.Model):
    class Meta:
        db_table = "categories"
        verbose_name = _("Категорія")
        verbose_name_plural = _("Категорії")
        ordering = ["category_number"]

    category_title = models.CharField(max_length=50, verbose_name=_('Назва категорії'))
    category_name = models.SlugField(verbose_name=_('Ім`я категорії транслітом'))
    menu_category = models.ForeignKey(MenuItem, related_name="categories", verbose_name=_("пункт меню"))
    category_number = models.IntegerField(verbose_name=_('Номер категорії'), default=1)
    category_url = models.CharField(max_length=200, verbose_name=_('Адреса для виконання'), blank=True)

    def __str__(self):
        return self.category_title

    def get_absolute_url(self):
        return reverse('blog:article_list', kwargs={'item_slug': self.menu_category.menu_name,
                                                    'category_slug': self.category_name})
