from django.test import TestCase
from django.core.urlresolvers import reverse
from articles.tests import create_article
    
class BackendIndexViewTests(TestCase):
    def test_view_with_no_articles(self):
        response = self.client.get(reverse("backend:index"))
        self.assertContains(response, "No articles are available")
        self.assertQuerysetEqual(response.context['latest_articles'], [])
    
    def test_view_with_multiple_past_and_multiple_future_article(self):
        create_article("past article", "", -5)
        create_article("very old article", "", -15)
        create_article("future article", "", 15)
        create_article("tomorrows article", "", 1)
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], ['<Article: future article>','<Article: tomorrows article>','<Article: past article>','<Article: very old article>'])

class ArticleDetailViewTests(TestCase):
    def test_view_with_past_article(self):
        article_past = create_article("past article", "past article content", -5)
        response = self.client.get(reverse("backend:detail", args=(article_past.id,)))
        self.assertContains(response, article_past.heading)
        self.assertContains(response, article_past.content)

    def test_view_with_future_article(self):
        article_future = create_article("future article", "future article content", 5)
        response = self.client.get(reverse("backend:detail", args=(article_future.id,)))
        self.assertContains(response, article_future.heading)
        self.assertContains(response, article_future.content)
        
class ArticleCreateViewTests(TestCase):
    def test_view_contains_heading_and_content(self):
        response = self.client.get(reverse("backend:create"))
        self.assertContains(response, "heading")
        self.assertContains(response, "content")
        
    def test_post_form_with_correct_data(self):
        response = self.client.post(reverse("backend:save"), {"heading":"my heading", "content":"my content"})
        self.assertTrue(response.status_code, 200)
        response = self.client.get(reverse("backend:index"))
        self.assertContains(response, "my heading")
        
    def test_post_form_with_to_short_heading(self):
        response = self.client.post(reverse("backend:save"), {"heading":"h", "content":"my content"})
        self.assertContains(response, "Error")
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], [])    
 
    def test_post_form_with_to_long_heading(self):
        response = self.client.post(reverse("backend:save"), {"heading":"h"*101, "content":"my content"})
        self.assertContains(response, "Error")
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], [])    
        
    def test_post_form_with_to_short_content(self):
        response = self.client.post(reverse("backend:save"), {"heading":"my heading", "content":"content"})
        self.assertContains(response, "Error")
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], [])
        
    def test_post_form_with_to_long_content(self):
        response = self.client.post(reverse("backend:save"), {"heading":"my heading", "content":"c"*501})
        self.assertContains(response, "Error")
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], [])
