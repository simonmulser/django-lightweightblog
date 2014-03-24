from django.test import TestCase
from django.core.urlresolvers import reverse
from articles.tests import create_article
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
 
NO_ARTICLES_STRING = "No articles are available"
VALID_HEADING = "My heading"
VALID_CONTENT = "My long content"
ERROR_MARKUP = 'class="errorlist"'

def login_test_user(self):
        self.adminuser = User.objects.create_user('admin', 'admin@test.com', 'pass')
        self.adminuser.save()
        self.client.login(username='admin', password='pass')
        
class BackendIndexViewTests(TestCase):
    
    def setUp(self):
        login_test_user(self)
        
    def test_view_with_no_articles(self):
        response = self.client.get(reverse("backend:index"))
        self.assertContains(response, NO_ARTICLES_STRING)
        self.assertQuerysetEqual(response.context['latest_articles'], [])
        
    
    def test_view_with_multiple_past_and_multiple_future_article(self):
        create_article("past article", "", -5)
        create_article("very old article", "", -15)
        create_article("future article", "", 15)
        create_article("tomorrows article", "", 1)
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], ['<Article: future article>','<Article: tomorrows article>','<Article: past article>','<Article: very old article>'])

class ArticleDetailViewTests(TestCase):
    
    def setUp(self):
        login_test_user(self)
        
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
        
class ArticleCreateTests(TestCase):
    
    def setUp(self):
        login_test_user(self)
    
    def test_view_contains_heading_and_content(self):
        response = self.client.get(reverse("backend:create"))
        self.assertContains(response, "heading")
        self.assertContains(response, "content")
        
    def test_form_create_with_correct_data(self):
        response = self.client.post(reverse("backend:create"), {"heading":VALID_HEADING, "content":VALID_CONTENT, "publication": timezone.now()})
        self.assertTrue(response.status_code, 200)
        response = self.client.get(reverse("backend:index"))
        self.assertContains(response, VALID_HEADING)
        
    def test_form_create_with_to_short_heading(self):
        response = self.client.post(reverse("backend:create"), {"heading":"h", "content":VALID_CONTENT, "publication": timezone.now()})
        self.assertContains(response, ERROR_MARKUP)
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], [])    
 
    def test_form_create_with_to_long_heading(self):
        response = self.client.post(reverse("backend:create"), {"heading":"h"*101, "content":VALID_CONTENT, "publication": timezone.now()})
        self.assertContains(response, ERROR_MARKUP)
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], [])    
        
    def test_form_create_with_to_short_content(self):
        response = self.client.post(reverse("backend:create"), {"heading":VALID_HEADING, "content":"content", "publication": timezone.now()})
        self.assertContains(response, ERROR_MARKUP)
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], [])
        
    def test_form_create_with_to_long_content(self):
        response = self.client.post(reverse("backend:create"), {"heading":VALID_HEADING, "content":"c"*501, "publication": timezone.now()})
        self.assertContains(response, ERROR_MARKUP)
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], [])
        
    def test_form_create_with_invalid_date(self):
        response = self.client.post(reverse("backend:create"), {"heading":VALID_HEADING, "content":"c"*501, "publication": "date"})
        self.assertContains(response, ERROR_MARKUP)
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], [])
        
class ArticleDeleteTests(TestCase):
    
    def setUp(self):
        login_test_user(self)
        
    def test_delete_existing_article(self):
        article = create_article("heading", "my long content", -5)
        response = self.client.post(reverse("backend:delete"), {"pk":article.id})
        self.assertTrue(response.status_code, 200)
        response = self.client.get(reverse("backend:index"))
        self.assertContains(response, NO_ARTICLES_STRING)
        
    def test_delete_not_existing_article(self):
        article = create_article("heading", "my long content", -5)
        response = self.client.post(reverse("backend:delete"), {"pk":article.id})
        self.assertTrue(response.status_code, 404)

    def test_delete_existing_article_with_other_existing_article(self):
        article_delete = create_article("heading", "my long content", -5)
        create_article("other heading", "my long content", -5)
        response = self.client.post(reverse("backend:delete"), {"pk":article_delete.id})
        self.assertTrue(response.status_code, 200)
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], ['<Article: other heading>'])
        
class ArticleEditTests(TestCase):
    
    def setUp(self):
        login_test_user(self)
        
    def test_if_fields_are_set(self):
        article = create_article("my heading", "my long content", -5)
        response = self.client.get(reverse("backend:edit", args=(article.id,)))
        self.assertContains(response, article.heading)
        self.assertContains(response, article.content)
        self.assertContains(response, article.publication.strftime('%Y-%m-%d %H:%M'))
        
    def test_form_edit_with_correct_data(self):
        article = create_article("my heading", "my long content", -5)
        response = self.client.post(reverse("backend:edit", args=(article.id,)), 
                                    {"heading":"new heading", "content":"new long content", "publication": timezone.now() + datetime.timedelta(days=5)})
        self.assertTrue(response.status_code, 200)
        response = self.client.get(reverse("backend:index"))
        self.assertQuerysetEqual(response.context['latest_articles'], ['<Article: new heading>'])

    def test_form_edit_with_wrong_pk(self):
        response = self.client.post(reverse("backend:edit", args=(1,)), 
                                    {"heading":"new heading", "content":"new long content", "publication": timezone.now() + datetime.timedelta(days=5)})
        self.assertTrue(response.status_code, 404)

        