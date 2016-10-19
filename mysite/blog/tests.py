from django.test import TestCase
from blog.models import Article


class ArticleTestCase(TestCase):

    # def test_article_image(self):
    #     article = Article(article_image='')
    #     self.assertEqual(article.get_image(), True)

    def test_article_image(self):
        articles = Article.objects.all()
        for article in articles:
            if not article.get_image():
                self.assertEqual(article.get_image(), True, '\nСтаття без картинки!\n')
