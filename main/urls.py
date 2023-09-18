from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    IndexView, 
    BookView, 
    LoginView, 
    PaymentSettingsChangeView, 
    DeleteBookView, 
    GetBookView, 
    BookmarkView, 
    PaymentView, 
    PaymentsView,
    PasswordResetView
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', IndexView.as_view()),
    re_path(r'^book/(?P<id>.*)$', csrf_exempt(BookView.as_view())),
    path('login', LoginView.as_view()),
    path('change_payment_settings', PaymentSettingsChangeView.as_view()),
    path('delete_book/<int:id>', DeleteBookView.as_view()),
    path('api/book/<int:id>', GetBookView.as_view()),
    path('api/bookmark', csrf_exempt(BookmarkView.as_view())),
    path('api/payment', csrf_exempt(PaymentView.as_view())),
    path('payments-history', PaymentsView.as_view(), name='payment_history'),
    path('reset-password', PasswordResetView.as_view(), name='reset_password')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)