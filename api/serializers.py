from rest_framework import serializers
from api.models import Book, Genre, Author, Reading
from .models import Post
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    apis = serializers.HyperlinkedRelatedField(many=True, view_name='api-detail', read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ("id", "h1", "title", "slug", "description", "content", "image", "created_at", "author", "tags")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


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

