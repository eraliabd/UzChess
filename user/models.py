from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin


from .managers import UserManager
from .choises import AuthTypeChoise


class CustomUser(AbstractBaseUser, PermissionsMixin):
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)

    phone_number = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    auth_type = models.CharField(
        max_length=100, choices=AuthTypeChoise.choices
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}-{self.phone_number}"

    @classmethod
    def is_phone_number_available(cls, phone_number):
        if cls.objects.filter(phone_number=phone_number).exists():
            return True
        return False

    @classmethod
    def is_email_available(cls, email):
        if cls.objects.filter(email=email).exists():
            return True
        return False

    @staticmethod
    def has_perm(perm, obj=None, **kwargs):
        return True

    @staticmethod
    def has_module_perms(app_label, **kwargs):
        return True

    @property
    def is_staff(self):
        return self.is_admin
