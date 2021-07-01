from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Book, Genre, Author, Reading, User


class BookSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='book-highlight', format='html')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        return Book(**validated_data)

    class Meta:
        model = Book
        fields = ['created', 'title', 'highlight', 'owner',
                  'description', 'genre_name', 'author_name', 'user', 'cover', 'pdf_file']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    apis = serializers.HyperlinkedRelatedField(many=True, view_name='api-detail', read_only=True)


    class Meta:
        model = User
        fields = ['url', 'id', 'user', 'apis']


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='genre-highlight', format='html')

    class Meta:
        model = Genre
        fields = ['genre_name', 'highlight', 'owner']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='author-highlight', format='html')

    class Meta:
        model = Author
        fields = ['author_name', 'highlight', 'owner']


class ReadingSerializer(serializers.HyperlinkedModelSerializer):
    reading = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='reading-highlight', format='html')

    class Meta:
        model = Reading
        fields = ['created', 'username', 'title', 'is_read', 'highlight', 'owner']

