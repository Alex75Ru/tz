from rest_framework import filters
from rest_framework import pagination
from rest_framework import permissions
from rest_framework import (viewsets, renderers, generics, status, mixins)
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import (Book, User, Genre, Author, Reading, Post)
from api.permissions import IsOwnerOrReadOnly
from api.serializers import BookSerializer
from api.serializers import (UserSerializer, GenreSerializer, AuthorSerializer, ReadingSerializer)
from .serializers import PostSerializer
from .serializers import RegisterSerializer


#TODO переделать на viewSet
class RegisterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        author = self.get_object()
        return Response(author.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewSet automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    This viewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        genre = self.get_object()
        return Response(genre.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    #TODO добавить фильтрацию по юзеру
class ReadingViewSet(viewsets.ModelViewSet):

    queryset = Reading.objects.filter()
    serializer_class = ReadingSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        model = serializer.save()
        serializer_view = self.get_serializer(model)
        return Response(serializer_view.data, status=status.HTTP_201_CREATED)





