from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    label = 'blog'
    verbose_name = 'Блог'

    def ready(self):
        import blog.signals.handlers



