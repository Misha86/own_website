from django.core.management.base import BaseCommand, CommandError
from blog.models import Article


class Command(BaseCommand):
    help = 'Closes the specified article for voting'

    def add_arguments(self, parser):
        parser.add_argument('article_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for article_id in options['article_id']:
            try:
                poll = Article.objects.get(pk=article_id)
            except Article.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % article_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed article "%s"' % article_id))