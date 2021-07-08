from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views
from django.conf import settings
from django.conf.urls.static import static

"""
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'reading', views.ReadingViewSet)
router.register(r'posts', views.PostViewSet, basename='posts')
#router.register(r'book_update', views.BookUpdateViewSet, basename='add_books')
"""
as_view_common = {"get": "list", "post": "create"}
as_view_with_pk = {"get": "retrieve", "put": "update", "delete": "destroy"}
#TODO Привести в порядок URLS.py

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('books/', views.BookViewSet.as_view(as_view_common)),
    path('books/<int:pk>/', views.BookViewSet.as_view(as_view_with_pk)),
    path('reading/', views.ReadingViewSet.as_view(as_view_common)),
    path('reading/<int:pk>/', views.ReadingViewSet.as_view(as_view_with_pk)),
    #path('books/', include(router.urls)),
    #path(r'reading/', include(router.urls)),
    #path('api/', include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token"),
    path("api/refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
    path("ckeditor/", include('ckeditor_uploader.urls')),
    path('register/', views.RegisterViewSet.as_view(as_view_common)),
    #path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

