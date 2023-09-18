from io import BytesIO

import boto3
from django.core.files.uploadedfile import UploadedFile
import uuid
from django.conf import settings
import os
import ebooklib
from ebooklib import epub


def upload_book_to_selectel(book: UploadedFile):
    s3 = boto3.client(
        's3',
        endpoint_url='https://s3.storage.selcloud.ru',
        region_name='ru-1',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    id = uuid.uuid4()
    with open(f'media/{book.name}', 'wb+') as f:
        for chunk in book.chunks():
            f.write(chunk)
    s3.upload_file(f'media/{book.name}', 'atlas', str(id))
    return id


def get_book_data(book: UploadedFile):
    ebook = epub.read_epub(f'media/{book.name}')
    os.remove(f'media/{book.name}')
    title = ebook.get_metadata("DC", "title")[0][0]

    author = ebook.get_metadata("DC", "creator")[0][0]
    image_content = None
    for image in ebook.get_items_of_type(ebooklib.ITEM_IMAGE):
        if "cover" in str(image):
            image_content = image
            break
    return title, author, image_content


def get_book_by_id(id: uuid.UUID):
    s3 = boto3.client(
        's3',
        endpoint_url='https://s3.storage.selcloud.ru',
        region_name='ru-1',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    data = s3.get_object(Bucket='atlas', Key=str(id))
    body = data['Body'].read()
    return body
