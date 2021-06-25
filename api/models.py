from django.db import models


class Book(models.Model):
    book_id = models.ForeignKey
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500))
    genre_id = models.TextField()
    author_id = models.TextField()
    user_id = models.BooleanField(default=False)
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
    full_name = models.TextField

    class Meta:
        ordering = ['full_name']


class Reading(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    read_id = models.ForeignKey
    user_id = models.BooleanField(default=False)
    book_id = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']



