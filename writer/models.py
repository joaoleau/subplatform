from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    content = models.TextField(max_length=10000, verbose_name=_("Content"))
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name=_("Date posted"))
    is_premium = models.BooleanField(default=False, verbose_name=_("Is this a premium article?"))
    user = models.ForeignKey(get_user_model(), max_length=10, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("writer:article-detail", kwargs={"pk": self.pk})
