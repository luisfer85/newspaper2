from django.db import models
from django.utils.translation import gettext_lazy as _

class News(models.Model):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    publish_date = models.DateTimeField(_('publish_date'))

    class Meta:
        verbose_name = _('news item')
        verbose_name_plural = _('news')

    def __str__(self):
        return self.title #Que queremos mostrar cuando listamos los elementos
