from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Book(models.Model):
    book_id = models.ForeignKey
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    genre_id = models.IntegerField()
    author_id = models.IntegerField()
    user_id = models.IntegerField()
    cover = models.ImageField()
    pdf_file = models.FileField()

    class Meta:
        ordering = ['created']


class Genre(models.Model):
    genre_id = models.ForeignKey
    genre_name = models.TextField()

    class Meta:
        ordering = ['genre_name']


class Author(models.Model):
    author_id = models.ForeignKey
    full_name = models.TextField()

    class Meta:
        ordering = ['full_name']


class Reading(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    read_id = models.ForeignKey
    user_id = models.ForeignKey
    book_id = models.ForeignKey
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']



