# Generated by Django 3.1.6 on 2021-02-28 14:50

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('content', models.TextField(max_length=5000)),
                ('slug', models.SlugField(editable=False, max_length=255)),
                (
                    'user_created',
                    models.ForeignKey(
                        default='c64c16ee-fc7f-45c3-a84b-a81a6a29d5d6',
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='blog_post_user_created_related',
                        related_query_name='blog_post_user_created_rquery',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='created by',
                    ),
                ),
                (
                    'user_updated',
                    models.ForeignKey(
                        default='c64c16ee-fc7f-45c3-a84b-a81a6a29d5d6',
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='blog_post_user_updated_related',
                        related_query_name='blog_post_user_updated_rquery',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='updated by',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]