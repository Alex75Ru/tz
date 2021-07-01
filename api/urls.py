from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views
from django.conf import settings
from django.conf.urls.static import static

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'posts', PostViewSet, basename='posts')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls))
    path("library/", include('api.urls')),
    path("api/token/", TokenObtainPairView.as_view(), name="token"),
    path("api/refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
    path("ckeditor/", include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
