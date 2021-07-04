from django.contrib import admin
from .models import Book, Genre, Author, Post, Reading

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Reading)
