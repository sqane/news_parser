from django.db import models
from django.utils.functional import cached_property

class News(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Заголовок')
    date_added = models.DateTimeField(verbose_name='Дата добавления')
    body = models.TextField(default='',
                            verbose_name='Тело статьи')

