from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpRequest
from . import services
from django.contrib import messages
import base64


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

    def get(self, request: HttpRequest, id: int, *args, **kwargs):
        response = ''
        book_data = None
        if not request.user.is_authenticated:
            response = 'Авторизуйтесь!'
        else:
            book_data, response = services.get_book_data(request.user, id)
        data = {
            'response': response,
            'book_data': book_data
        }
        return render(request, self.template_name, data)


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