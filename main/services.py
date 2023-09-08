from django.core.files.uploadedfile import UploadedFile
from django.http import QueryDict
from .forms import RegisterForm
from .models import User, Book
import uuid
from . import utils


def register_user(post: QueryDict):
    form = RegisterForm(post)
    if form.is_valid():
        new_user: User = form.save(commit=False)
        raw_password = User.objects.make_random_password()
        new_user.set_password(raw_password)
        new_user.save()
        new_user.email_user(
            'Информация о пользователе!',
            f'Вот ваши данные для входа:\nПочта: {new_user.email}\nПароль: {raw_password}',
            None
        )
        return "Вам на почту пришли новые данные для входа!"
    return 'Не удалось отправить сообщение, повторите попытку позже!'


def get_books_by_user(user: User) -> list[Book]:
    books = Book.objects.all().filter(user=user)
    return books


def upload_book(user: User, book: UploadedFile):
    boto3_id = utils.upload_book_to_selectel(book)
    title, author, image = utils.get_book_data(book)
    book = Book(user=user, title=title, author=author, boto3_id=boto3_id)
    book.save()
    return 'Ваша книга была успешно загружена!'


def get_book_data(user: User, id: int):
    book = Book.objects.get(id=id)
    if book.user != user:
        return None, 'Доступ запрещен!'
    book_file = utils.get_book_by_id(book.boto3_id)
    return book_file, ''


def change_email(user: User, email: str, password: str):
    if not user.check_password(password):
        return '', 'Неправильный пароль!'
    user.email = email
    user.save()
    return 'Почта успешно изменена!', ''


def change_password(user: User, old_password: str, new_password: str):
    if not user.check_password(old_password):
        return '', 'Неправильный пароль!'
    user.set_password(new_password)
    user.save()
    return 'Пароль успешно изменен!', ''