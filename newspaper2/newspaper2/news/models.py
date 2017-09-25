from django.db import models
from django.utils.translation import gettext_lazy as _

from newspaper2.news.managers import NewsManager


class BaseNews(models.Model):
    title = models.CharField(_('title'), max_length=255, help_text='Hola Mundo')
    description = models.TextField(_('description'), blank=True, null=True)
    publish_date = models.DateTimeField(_('publish_date'))

    objects = NewsManager()

    class Meta:
        abstract = True #Evita crear una tabla para esta clase de tal manera que estos campos se incluyen en las tablas heredadas

    def __str__(self):
        return self.title #Que queremos mostrar cuando listamos los elementos

class News(BaseNews):

    class Meta:
        verbose_name = _('news item')
        verbose_name_plural = _('news')

class Event(BaseNews):
    start_date = models.DateTimeField(_('start_date'))
    end_date = models.DateTimeField(_('end_date'))

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
