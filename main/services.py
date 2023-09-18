import io

from django.core.files.uploadedfile import UploadedFile
from django.core.files.images import ImageFile
from django.http import QueryDict
from django.utils import timezone

from .forms import RegisterForm
from .models import User, Book, BookMark, Deposit, SubscriptionPayment
import uuid
from . import utils
from django.conf import settings


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
    preview_image = ImageFile(io.BytesIO(image.content), f'{title}_{image.file_name}')
    book = Book(user=user, title=title, author=author, boto3_id=boto3_id, preview_image=preview_image)
    book.save()
    return 'Ваша книга была успешно загружена!'


def get_book_data(user: User, id: int):
    book = Book.objects.get(id=id)
    if book.user != user:
        return None
    book_file = utils.get_book_by_id(book.boto3_id)
    return book_file


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


def change_payment_settings(user: User, form: dict):
    if 'payment_active' in form and not user.payment_active and not user.is_paid:
        if user.balance >= settings.SUBSCRIPTION_PRICE:
            user.balance -= settings.SUBSCRIPTION_PRICE
            new_subscription_payment = SubscriptionPayment(user=user)
            new_subscription_payment.save()
            user.is_paid = True
            user.last_payment = timezone.now()
            user.payment_active = True
        else:
            return '', 'Недостаточно средств, пополните баланс!'
    elif 'payment_active' in form and user.is_paid:
        user.payment_active = True
    elif 'payment_active' not in form and user.payment_active:
        user.payment_active = False
    user.save()
    return '', ''


def delete_book(user: User, id: int):
    book = Book.objects.get(id=id)
    if not book:
        return '', 'Книга не найдена!'
    if book.user != user:
        return '', 'Нет доступа!'
    book.delete()
    return 'Книга успешно удалена!', ''


def get_book_by_id(id: int):
    print(id)
    book = Book.objects.get(id=id)
    return book


def get_bookmarks_by_book_id(id: int):
    bookmarks = BookMark.objects.all().filter(book__id=id).order_by('id')[::-1]
    return bookmarks


def update_book_by_id(id: int, data: dict):
    book = Book.objects.filter(id=id).update(**data)
    return


def create_bookmark(data: dict):
    if data['name'] == '':
        data['name'] = 'Без названия'
    bookmark = BookMark(name=data['name'], book_id=data['book_id'], location=data['location'])
    bookmark.save()
    return bookmark


def delete_bookmark(user: User, id: int) -> (bool, str):
    print(id)
    bookmark = BookMark.objects.get(id=int(id))
    if bookmark.book.user != user:
        return False, 'Нет доступа!'
    bookmark.delete()
    return True, 'Закладка удалена!'


def create_payment(user: User, data: dict) -> uuid.UUID:
    new_payment = Deposit(id=uuid.uuid4(), user=user, amount=data.get('amount'))
    new_payment.save()
    return new_payment.id


def update_payment(user: User, data: dict) -> (bool, str):
    payment = Deposit.objects.filter(id=data.get('id')).first()
    if not payment:
        return False, 'Платеж не найден!'
    if not data.get('success'):
        return False, 'Не удалось пополнить баланс!'
    payment.success = data.get('success')
    if payment.success:
        user.balance += payment.amount
    payment.save()
    user.save()
    return True, 'Баланс успешно пополнен!'


def get_all_payments(user: User):
    subscriptions = SubscriptionPayment.objects.all().filter(user=user)
    deposits = Deposit.objects.all().filter(user=user)
    payments = list(subscriptions) + list(deposits)
    return sorted(payments, key=lambda x: x.created_at, reverse=True)

def reset_password(email: str):
    user = User.objects.filter(email=email).first()
    if not user:
        return '', 'Пользователь с такой почтой не найден!'
    raw_password = User.objects.make_random_password()
    user.set_password(raw_password)
    user.save()
    user.email_user(
            'Новые данные для входа!',
            f'Вот ваши данные для входа:\nПочта: {user.email}\nПароль: {raw_password}',
            None
        )
    return 'Вам на почту был выслан новый пароль!', ''