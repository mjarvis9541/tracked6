from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from utils.behaviours import Authorable, Timestampable, Uuidable


class Post(Authorable, Timestampable, Uuidable):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(max_length=5000)
    slug = models.SlugField(max_length=255, editable=False)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ('-datetime_created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        slug_str = f'{self.title}'
        self.slug = slugify(slug_str)
        super().save(*args, **kwargs)
