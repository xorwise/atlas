from django.urls import path
from .views import IndexView, BookView, LoginView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', IndexView.as_view()),
    path('book/<int:id>', BookView.as_view()),
    path('login', LoginView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)