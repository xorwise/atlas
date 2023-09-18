from django.contrib import admin
from .models import User, Book, BookMark, SubscriptionPayment, Deposit

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookMark)
admin.site.register(SubscriptionPayment)
admin.site.register(Deposit)
