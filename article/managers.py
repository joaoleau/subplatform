from django.db import models
from django.db.models.query import QuerySet


class ArticleQuerySet(models.QuerySet):

    def standard(self):
        return self.exclude(access_level="Premium")


class ArticleManager(models.Manager):

    def public_articles(self):
        return self.exclude(access_level="Private")

    def private_articles(self):
        return self.filter(access_level="Private")

    def get_queryset(self) -> QuerySet:
        return ArticleQuerySet(self.model, using=self._db)
