from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views
from library import settings

as_view_common = {"get": "list", "post": "create"}
as_view_get = {"get": "list"}
as_view_with_pk = {"get": "retrieve", "put": "update", "delete": "destroy"}
#TODO Привести в порядок URLS.py

urlpatterns = [
    path('books/', views.BookViewSet.as_view(as_view_common)),
    path('books/<int:pk>/', views.BookViewSet.as_view(as_view_with_pk)),
    path('reading/', views.ReadingViewSet.as_view(as_view_common)),
    path('reading/<int:pk>/', views.ReadingViewSet.as_view(as_view_with_pk)),
    path('reading_rating/', views.ReadingRatingViewSet.as_view(as_view_get)),
    path("api/token/", TokenObtainPairView.as_view(), name="token"),
    path("api/refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
    path("ckeditor/", include('ckeditor_uploader.urls')),
    path('register/', views.RegisterViewSet.as_view(as_view_common)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

