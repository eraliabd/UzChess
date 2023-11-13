from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import CustomUser as User


class Category(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    image = models.ImageField(upload_to='Category')
    cours_count = models.IntegerField()


class Course(models.Model):
    Degre = (
        ('boshlangich', 'Boshlangich'),
        ('profesional', 'Profesional'),
        ('havaskor', 'Havaskor'),
    )
    title = models.CharField(_("Title"), max_length=255)
    price = models.IntegerField()
    image = models.ImageField(upload_to='Course')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    degree = models.CharField(max_length=50, choices=Degre)

    rating = models.FloatField()

    section_count = models.IntegerField()
    lesson_count = models.IntegerField()
    comment_count = models.IntegerField()

    def __str__(self) -> str:
        return self.title


class Lesson(models.Model):
    cours = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=255)
    text = models.TextField(_("Text"))
    url = models.URLField()
    image = models.ImageField(upload_to='Lesson')


class Comment(models.Model):
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField(_("Text"))
    rate = models.IntegerField()


class Complaint(models.Model):
    demo = (
        ('yomon_mavzu', 'Yomon mavzu'),
        ('yomon_ustoz', 'Yomon ustoz'),
        ('yomon_sayt', 'Yomon sayt'),
    )
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)
    cours = models.ForeignKey(Course, on_delete=models.CASCADE)
    complaint = models.CharField(max_length=50, choices=demo)
    text = models.CharField(_("Text"), max_length=300)
