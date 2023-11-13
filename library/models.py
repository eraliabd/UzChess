from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField

from utils.models import BaseModel


class DegreeChoice(models.TextChoices):
    amateur = _("Havaskor")
    initial = _("Boshlang'ich")
    professional = _("Professional")


class Author(models.Model):
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class BookCategory(models.Model):
    title = models.CharField(_("Title"), max_length=255)

    def __str__(self):
        return self.title


class Book(BaseModel):
    # relations
    category = models.ForeignKey(
        BookCategory, on_delete=models.CASCADE, related_name='books'
    )
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='author_books'
    )

    # choice fields
    degree = models.CharField(
        max_length=20, choices=DegreeChoice.choices, default=DegreeChoice.initial
    )

    # fields
    title = models.CharField(_("Title"), max_length=255)
    image = models.ImageField(upload_to='book_images/')
    content = RichTextUploadingField(_("Content"))
    price = models.FloatField()
    old_price = models.FloatField()
    number_of_pages = models.IntegerField()
    is_top = models.BooleanField(default=False)
    is_recommend = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} - {self.title}"
