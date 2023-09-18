from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from django.http import HttpRequest
from . import services
from django.contrib import messages
import base64
from django.core.serializers import serialize
import json


# Create your views here.
class IndexView(View):
    template_name = 'index.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        books = list()
        if request.user.is_authenticated:
            books = services.get_books_by_user(request.user)
            print(books)
        data = {
            'books': books
        }
        return render(request, self.template_name, data)

    # noinspection PyArgumentList
    def post(self, request: HttpRequest, *args, **kwargs):
        exception_detail = ''
        response = ''
        match list(request.POST.keys()):
            case [*_, 'register']:
                if request.user.is_authenticated:
                    exception_detail = 'Вы уже авторизованы!'
                else:
                    response = services.register_user(request.POST)
            case [*_, 'delete_account']:
                request.user.delete()
            case [*_, 'change_email']:
                if not request.user.is_authenticated:
                    exception_detail = 'Авторизуйтесь, чтобы загрузить книгу!'
                else:
                    response, exception_detail = services.change_email(
                        request.user,
                        request.POST.get('new_email'),
                        request.POST.get('password')
                    )
            case [*_, 'change_password']:
                if not request.user.is_authenticated:
                    exception_detail = 'Авторизуйтесь, чтобы загрузить книгу!'
                else:
                    response, exception_detail = services.change_password(
                        request.user,
                        request.POST.get('old_password'),
                        request.POST.get('new_password')
                    )
            case [*_, 'change_payment_settings']:
                if not request.user.is_authenticated:
                    exception_detail = 'Авторизуйтесь, чтобы загрузить книгу!'
                else:
                    response, exception_detail = services.change_payment_settings(request.user, request.POST)

        if 'book' in request.FILES:
            if not request.user.is_authenticated:
                exception_detail = 'Авторизуйтесь, чтобы загрузить книгу!'
            else:
                response = services.upload_book(request.user, request.FILES.get('book'))
        messages.info(request, response)
        messages.error(request, exception_detail)
        return HttpResponseRedirect('/')


class BookView(View):
    template_name = 'ePubViewer/index.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        response = ''
        exception_detail = ''
        id = request.GET.get('id', '')

        if not request.user.is_authenticated:
            exception_detail = 'Авторизуйтесь!'
        book = bookmarks = None
        if id != '':
            book = serialize('json', [services.get_book_by_id(int(id))])
            bookmarks = services.get_bookmarks_by_book_id(int(id))
        data = {
            'book': book,
            'bookmarks': bookmarks,
            'json_bookmarks': serialize('json', bookmarks),
            'exception_detail': exception_detail,
            'response': response,
        }
        return render(request, self.template_name, data)

    def put(self, request: HttpRequest, *args, **kwargs):
        id = request.GET.get('id', '')
        data = json.loads(request.body)
        services.update_book_by_id(id, data)
        return HttpResponse('Success!')

class LoginView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        else:
            messages.error(request, 'Неправильный E-mail или пароль!')

        return HttpResponseRedirect('/')


class PaymentSettingsChangeView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        print()


class DeleteBookView(View):
    def post(self, request: HttpRequest, id: int, *args, **kwargs):
        response = ''
        if not request.user.is_authenticated:
            exception_detail = 'Авторизуйтесь!'
        else:
            reponse, exception_detail = services.delete_book(request.user, id)

        messages.error(request, exception_detail)
        messages.info(request, response)
        return HttpResponseRedirect('/')


class GetBookView(View):
    def get(self, request: HttpRequest, id: int, *args, **kwargs):
        book_data = None

        if request.user.is_authenticated and id:
            book_data = services.get_book_data(request.user, int(id))
        if book_data:
            name = services.get_book_by_id(id)
            response = HttpResponse(book_data, content_type='application/epub+zip')
            response['Content-Disposition'] = f'attachment; filename="{name}.epub"'
        else:
            response = HttpResponseNotFound('<h1>File not exist</h1>')
        return response


class BookmarkView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        data = json.loads(request.body)
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Авторизуйтесь!')
        new_bookmark = services.create_bookmark(data)
        return HttpResponse(serialize('json', [new_bookmark]))

    def delete(self, request: HttpRequest, *args, **kwargs):
        
        data = json.loads(request.body)
        print(data)
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Авторизуйтесь!')
        
        status, text = services.delete_bookmark(request.user, data.get('id'))
        if not status:
            return HttpResponseNotFound(text)
        return HttpResponse(text)


class PaymentView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        data = json.loads(request.body)
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Авторизуйтесь!')
        
        id = services.create_payment(request.user, data)
        print(id)
        if not id:
            return HttpResponseServerError('Не удалось создать платеж!')
        return HttpResponse(json.dumps({'id': str(id)}))

    def patch(self, request: HttpRequest, *args, **kwargs):
        data = json.loads(request.body)

        status, response = services.update_payment(request.user, data)
        if not status:
            return HttpResponseServerError(response)
        return HttpResponse(response)


class PaymentsView(View):
    template_name = 'payment_history.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Авторизуйтесь!')
        
        payments = services.get_all_payments(request.user)
        print(len(payments))
        return render(request, self.template_name, {'payments': payments})
        
        
class PasswordResetView(View):
    template_name = 'password_reset.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        email = request.POST.get('email')
        response, exception_detail = services.reset_password(email)

        messages.info(request, response)
        messages.error(request, exception_detail)
        return render(request, self.template_name)

