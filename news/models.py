from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField

from utils.models import BaseModel

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(_("Title"), max_length=255)

    def __str__(self):
        return self.title


class New(BaseModel):
    # relations
    tag = models.ManyToManyField(Tag)

    # fields
    title = models.CharField(_("Title"), max_length=255)
    image = models.ImageField(upload_to='news_images/')
    content = RichTextUploadingField(_("Content"))
    view = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class NewsView(BaseModel):
    device_id = models.CharField(max_length=200)
    news = models.ForeignKey(New, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.device_id
