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
    name = models.CharField(verbose_name='Жанр', default='Поэма', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Author(models.Model):
    name = models.CharField(verbose_name='Автор', default='Александр Пушкин', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    # TODO добавить функцию для создания каталога для картинки по имени модели и для файла в пдф
    # Обошёлся встроенным параметром upload_to и добавил разбиение по годам и месяцам
    # Для добавления разбиения по дням необходимо будет добавить /%d
class Book(models.Model):
    created = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    title = models.CharField(verbose_name='Название', max_length=100)
    description = RichTextUploadingField(verbose_name='Описание', max_length=500)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    author = models.ManyToManyField(Author, verbose_name='Автор')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='book/images/%Y/%m', verbose_name='Обложка')
    pdf_file = models.FileField(upload_to='book/pdfs/%Y/%m', verbose_name='Книга в формате PDF')

    def __str__(self):
        return self.title


class Reading(models.Model):
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    title = models.ForeignKey(Book, verbose_name='Книга', on_delete=models.CASCADE)
    is_read = models.BooleanField(verbose_name='Прочитано', default=False)

    class Meta:
        ordering = ['title']