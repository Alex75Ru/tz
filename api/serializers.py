from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Book, Genre, Author, Reading


class BookSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='book-highlight', format='html')

    class Meta:
        model = Book
        fields = ['book_id', 'created', 'created', 'title', 'highlight', 'owner',
                  'description', 'genre_id', 'author_id', 'user_id', 'cover', 'pdf_file']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    apis = serializers.HyperlinkedRelatedField(many=True, view_name='api-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'books']


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='genre-highlight', format='html')

    class Meta:
        model = Genre
        fields = ['genre_id', 'genre_name', 'highlight', 'owner']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='author-highlight', format='html')

    class Meta:
        model = Author
        fields = ['author_id', 'full_name', 'highlight', 'owner']


class ReadingSerializer(serializers.HyperlinkedModelSerializer):
    reading = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='reading-highlight', format='html')

    class Meta:
        model = Reading
        fields = ['created', 'read_id', 'user_id', 'book_id', 'is_read', 'highlight', 'owner']

