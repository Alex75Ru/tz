from django.db.models import Count, Case, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from rest_framework import (viewsets, status)
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import (Book, User, Genre, Author, Reading, Post)
from api.permissions import IsOwnerOrReadOnly
from api.serializers import BookSerializer, ReadingRatingSerializer
from api.serializers import (UserSerializer, GenreSerializer, AuthorSerializer, ReadingSerializer)
from .serializers import PostSerializer, RegisterSerializer


class RegisterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'h1']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    """
    This viewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class AuthorViewSet(viewsets.ModelViewSet):
    """
    This viewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminUser]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewSet automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GenreViewSet(viewsets.ModelViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAdminUser]


    #TODO добавить фильтрацию по юзеру
    # добавил проверку на пользователя, теперь редактировать свой список прочтения может только владелец
class ReadingViewSet(viewsets.ModelViewSet):

    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        model = serializer.save()
        serializer_view = self.get_serializer(model)
        return Response(serializer_view.data, status=status.HTTP_201_CREATED)


#TODO рейтинг книг
#TODO сделать через агрегацию и аннотацию
class ReadingRatingViewSet(viewsets.ModelViewSet):
    # Рейтинг прочитанных книг
    queryset = Book.objects.all().annotate(count_reading=Count(Case(When(reading__is_read=True, then=1))))
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['count_reading', 'title']
    serializer_class = ReadingRatingSerializer
    permission_classes = [AllowAny]


"""class ReadingWishRatingViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        sql_query = "SELECT title_id as id, count(created) as count_reading FROM api_reading where is_read = 'False'" \
                    " GROUP BY title_id ORDER BY count(created) DESC"
        return Reading.objects.raw(sql_query)

    serializer_class = ReadingRatingSerializer
    permission_classes = [AllowAny]"""


#TODO сделать через агрегацию и аннотацию
class ReadingWishRatingViewSet(viewsets.ModelViewSet):
    # Рейтинг выбранных книг, но не прочитанных
    queryset = Book.objects.all().annotate(count_reading=Count(Case(When(reading__is_read=False, then=1))))
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['count_reading', 'title']
    serializer_class = ReadingRatingSerializer
    permission_classes = [AllowAny]


# Личный список пользователя для чтения
class ReadingListViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return Reading.objects.filter(user=user)

    serializer_class = ReadingSerializer
    permission_classes = [IsOwnerOrReadOnly]
