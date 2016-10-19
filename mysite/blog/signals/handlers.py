from django.db.models.signals import pre_save
from blog.models import Article
from django.utils.text import slugify
from django.dispatch import receiver


def create_slug(instance, new_slug=None):
    slug = slugify(instance.article_title, allow_unicode=True)
    if new_slug is not None:
        slug = new_slug
    qs = Article.objects.filter(article_slug=slug)
    exists = qs.exists()
    if exists:
        # update slug
        if instance in qs:
            return slug
        # update slug with id
        if instance.id:
            slug = "{}-{}".format(slug, instance.id)
            return slug
        # create slug with id
        else:
            a_id = Article.objects.all().order_by("-id").first().id + 1
            new_slug = "{}-{}".format(slug, a_id)
            return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Article, dispatch_uid="my_article_slug")
def pre_save_article_receiver(sender, instance, *args, **kwargs):
    instance.article_slug = create_slug(instance)


                       # АБО ТАК

# def pre_save_article_receiver(sender, instance, *args, **kwargs):
#     instance.article_slug = create_slug(instance)
#
#
# pre_save.connect(pre_save_article_receiver, sender=Article)
