from datetime import datetime

from django.db import models
from django.db.models.query import QuerySet


class NewsQuerySet(QuerySet):

    def published(self):
        return self.filter(publish_date__lte=datetime.now()).order_by('-publish_date')


class NewsManager(models.Manager):

    def get_queryset(self):
        return NewsQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()