from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import six
from django.test import TestCase
from django.test.client import Client

from newspaper2.news.models import News

class NewsTestCase(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def authentication(self):
        user, is_created = User.objects.get_or_create(username='admin')
        if is_created:
            user.is_superuser = True
            user.set_password('admin')
            user.save()
        self.client.login(username='admin', password='admin')

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

    def test_news_add(self):
        self.authentication()
        response1 = self.client.get(reverse('news_add'))
        self.assertEqual(response1.status_code, 200)
        self.assertIn(b'Texto de ayuda', response1.content)

        news_title = 'Mi noticia test 2'
        news_description = 'Mi descripcion test 2'
        data = {'title': news_title,
                'description': news_description,
                'publish_date': datetime.now()}
        response2 = self.client.post(reverse('news_add'),
                                     data=data)
        self.assertEqual(response2.status_code, 302)

        response3 = self.client.get(reverse('news_list'))
        self.assertIn(b'Mi noticia test 2', response3.content)
        self.assertIn(b'Mi descripcion test 2', response3.content)

        response4 = self.client.post(reverse('news_add'),
                                     data={})
        self.assertEqual(response4.status_code, 200)
        self.assertIn(b'Este campo es obligatorio.', response4.content)

    def test_print_news(self):
        news = News.objects.create(title='Mi noticia impresion test',
                                   description='Mi descripcion impresion test',
                                   publish_date=datetime.now())
        self.assertEqual(news.title, six.text_type(news))  #Se utiliza news.title porque en el modelo pusimos "return self.title"