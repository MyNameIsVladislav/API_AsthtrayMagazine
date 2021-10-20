# Generated by Django 3.2.6 on 2021-10-19 09:27

import articleapp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Not found', max_length=70, verbose_name='title')),
                ('short_describe', models.TextField(default='Not Found', max_length=150, verbose_name='short describe')),
                ('slug', models.SlugField(max_length=70, unique_for_date='publish')),
                ('text', models.TextField(null=True, verbose_name='text')),
                ('img_mini', models.ImageField(upload_to=articleapp.models.choose_path, verbose_name='image mini')),
                ('img_main', models.ImageField(upload_to=articleapp.models.choose_path, verbose_name='image main')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='CommentsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, max_length=5, verbose_name='status')),
                ('text', models.TextField(max_length=200, verbose_name='comment')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articleapp_commentsmodel', to='articleapp.articlemodel', verbose_name='article')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='genre')),
                ('slug', models.SlugField(verbose_name='slug')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='authors')),
            ],
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='genres_id',
            field=models.ManyToManyField(related_name='genres', related_query_name='genre', to='articleapp.Genres'),
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='owner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner', to='articleapp.author', verbose_name='owner'),
        ),
        migrations.CreateModel(
            name='ModelLikesComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, max_length=5, verbose_name='status')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articleapp_modellikescomment', to='articleapp.articlemodel', verbose_name='article')),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articleapp.commentsmodel')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'unique_together': {('user_id', 'comment_id')},
            },
        ),
        migrations.CreateModel(
            name='ModelLikesArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, max_length=5, verbose_name='status')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articleapp_modellikesarticle', to='articleapp.articlemodel', verbose_name='article')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'unique_together': {('user_id', 'article_id')},
            },
        ),
    ]
