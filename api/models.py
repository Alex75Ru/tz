from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Post(models.Model):
    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Genre(models.Model):
    genre_name = models.TextField()

    def __str__(self):
        return self.genre_name

    class Meta:
        ordering = ['genre_name']


class Author(models.Model):
    author_name = models.CharField(verbose_name='Прочитано', default='Александр Пушкин', max_length=100)

    def __str__(self):
        return self.author_name

    class Meta:
        ordering = ['author_name']


class Book(models.Model):
    created = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    title = models.CharField(verbose_name='Название', max_length=100)
    description = RichTextUploadingField(verbose_name='Описание', max_length=500)
    genre_name = models.ForeignKey(Genre, verbose_name='Жанр', max_length=100, on_delete=models.CASCADE)
    author_name = models.ForeignKey(Author, verbose_name='Автор', max_length=100, on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', max_length=100, on_delete=models.CASCADE)
    cover = models.ImageField(verbose_name='Обложка')
    pdf_file = models.FileField(verbose_name='Книга в формате PDF')

    def __str__(self):
        return self.title

    def perform_create(self):
        pass

    class Meta:
        ordering = ['created']


class Reading(models.Model):
    created = models.DateTimeField(verbose_name='Жанр', auto_now_add=True, max_length=100)
    username = models.ForeignKey(User, verbose_name='Пользователь', max_length=100, on_delete=models.CASCADE)
    title = models.ForeignKey(Book, verbose_name='Книга', max_length=100, on_delete=models.CASCADE)
    is_read = models.BooleanField(verbose_name='Прочитано', default=False)

    class Meta:
        ordering = ['created']