from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, full_name=None, password=None,):
        # if not email or phone_number:
        #     return ValueError('Error')

        if not password:
            raise ValueError("Error")

        user = self.model(
            email=self.normalize_email(email=email),
            phone_number=phone_number,
            full_name=full_name
        )

        user.set_password(password)  # change password to hash
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, full_name=None, password=None,):
        user = self.create_user(
            phone_number=phone_number,
            full_name=full_name,
            email=email,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(
            models.Q(email__iexact=username) |
            models.Q(phone_number__iexact=username)
        )
