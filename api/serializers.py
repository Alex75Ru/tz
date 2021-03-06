from rest_framework import serializers, status
from rest_framework.response import Response

from api.models import Book, Genre, Author, Reading
from .models import Post
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User

from .utils import check_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # TODO Выписать все нужные поля
        # Можно ещё добавить встроенные first_name & last_name если потребуется
        fields = ("id", 'username', 'email')


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

    def validate(self, attrs):
        password = attrs["password"]
        if not check_password(password):
            raise serializers.ValidationError({"password": "Необходим более сложный пароль: минимум 8 знаков, "
                                                           "должны быть цифры, строчные и заглавные буквы"})
        password2 = attrs["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают!"})

        return attrs

    #TODO Вынести проверку в функцию  валидации
    # перенес в функцию validate
    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
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


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id']


class BookSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = AuthorSerializer(read_only=True, many=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ['id', 'created', 'title',
                  'description', 'genre', 'author', 'user', 'cover', 'pdf_file']


class ReadingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reading
        fields = ['created', 'user', 'title', 'is_read']


class ReadingRatingSerializer(serializers.ModelSerializer):

    count_reading = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['count_reading', 'title']




