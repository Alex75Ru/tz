from django.conf.urls import url
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
router.register(r'reading', views.ReadingViewSet)
router.register(r'posts', views.PostViewSet, basename='posts')
#router.register(r'book_update', views.BookUpdateViewSet, basename='add_books')





# The API URLs are now determined automatically by the router.
urlpatterns = [
    #path('book_update/', include(router.urls)),
    path(r'reading/', include(router.urls)),
    path('api/', include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token"),
    path("api/refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
    path("ckeditor/", include('ckeditor_uploader.urls')),
    path('register/', views.RegisterView.as_view()),
    path(r'reading/', include(router.urls)),
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

