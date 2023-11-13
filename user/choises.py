from django.db import models


class AuthTypeChoise(models.Choices):
    phone_number = 'PhoneNumber'
    email = 'Email'
