from django.contrib import admin
from navigation.models import Category, MenuItem
from blog.models import Article
from django.utils.translation import ugettext_lazy as _


class MenuItemInLine(admin.StackedInline):
    model = Category
    prepopulated_fields = {"category_name": ("category_title",)}
    extra = 1
    verbose_name = _("Список категорий пункту меню")


class MenuItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"menu_name": ("menu_title",), }
    list_display = ('menu_title', 'menu_number', 'menu_type')
    ordering = ('menu_number',)
    inlines = [MenuItemInLine]


class CategoryInline(admin.StackedInline):
    model = Article
    extra = 1
    verbose_name = _("Список статей даної категорії")


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"category_name": ("category_title",)}
    list_display = ('category_title', 'menu_category')
    inlines = [CategoryInline]


admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Category, CategoryAdmin)
