from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from newspaper2.news.models import News

class NewsTestCase(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    # Crea aqui tus test. Se ejecutaran por orden alfabetico y siempre tienen que empezar con la palabra test.
    def test_newslist(self):
        news = News.objects.create(title=b'Mi noticia test',
                                   description=b'Mi descripcion test',
                                   publish_date=datetime.now())
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(news.title, response.content)
        self.assertIn(news.description, response.content)
        self.assertNotIn(b'ESTA CADENA NO SE ENCUENTRA EN EL RESPONSE',
                         response.content)
