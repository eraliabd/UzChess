import datetime
from django.db import models
from django.utils.crypto import get_random_string

from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel
from user.models import CustomUser as User
from course.models import Course
from library.models import Book


class CartItem(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_cart_item'
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + ') ' + self.book.title + ' ' + str(self.quantity)


class OrderStatusChoice(models.Choices):
    pending = _("Pending")
    delivered = _("Delivered")
    canceled = _("Canceled")


class Order(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders'
    )
    orders = models.ManyToManyField(
        CartItem
    )

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    status = models.CharField(
        max_length=50, choices=OrderStatusChoice.choices, default=OrderStatusChoice.pending
    )

    def __str__(self):
        return f"{self.full_name} {self.phone_number} {self.status}"
