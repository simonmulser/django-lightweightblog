import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from articles.models import Article


def create_article(heading, content, days):
    return Article.objects.create(heading = heading, content = content,
                                  publication=timezone.now() + datetime.timedelta(days=days))

class ArticlesMethodsTests(TestCase):
    def test_is_published_with_future_article(self):
        future_article = Article(publication=timezone.now() + datetime.timedelta(days=1))
        self.assertEqual(future_article.is_published(), False)
        
    def test_is_published_with_past_article(self):
        past_article = Article(publication=timezone.now() + datetime.timedelta(days=-1))
        self.assertEqual(past_article.is_published(), True)
    
class ArticleIndexViewTests(TestCase):
    def test_view_with_no_articles(self):
        response = self.client.get(reverse("articles:index"))
        self.assertContains(response, "No articles are available")
        self.assertQuerysetEqual(response.context['latest_articles'], [])
        
    def test_view_with_a_past_and_a_future_article(self):
        create_article("past article", "", -5)
        create_article("future article", "", 5)
        response = self.client.get(reverse("articles:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], ['<Article: past article>'])
    
    def test_view_with_multiple_past_and_multiple_future_article(self):
        create_article("past article", "", -5)
        create_article("very old article", "", -15)
        create_article("future article", "", 15)
        create_article("future article", "", 5)
        response = self.client.get(reverse("articles:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], ['<Article: past article>','<Article: very old article>'])

class ArticleDetailViewTests(TestCase):
    def test_view_past_article(self):
        article_past = create_article("past article", "past article content", -5)
        response = self.client.get(reverse("articles:detail", args=(article_past.id,)))
        self.assertContains(response, article_past.heading)
        self.assertContains(response, article_past.content)

    def test_view_future_article(self):
        article_future = create_article("future article", "", 5)
        response = self.client.get(reverse("articles:detail", args=(article_future.id,)))
        self.assertEqual(response.status_code, 404)