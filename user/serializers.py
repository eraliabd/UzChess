from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import CustomUser


class RegisterUserPhoneNumberSerailzier(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'phone_number',
        ]

    def validate(self, data):
        phone_number = data.get('phone_number', None)
        # email = data.get('email', None)

        if phone_number is not None:
            if CustomUser.is_phone_number_available(phone_number=phone_number):
                raise ValidationError(
                    {"phone_number": _("This number is already taken")}
                )
            data.update({"auth_type": 'phone_number'})
            return data

        raise ValidationError(
            {
                "error": _("You must enter phone number!"),
            }
        )


class RegisterUserEmailSerailzier(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
        ]

    def validate(self, data):
        email = data.get('email', None)
        # email = data.get('email', None)

        if email is not None:
            if CustomUser.is_email_available(email=email):
                raise ValidationError(
                    {"email": _("This email is already taken")}
                )
            data.update({"auth_type": 'email'})
            return data
        raise ValidationError(
            {
                "error": _("You must enter email!"),
            }
        )


class VerifyPhoneNumberCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()
    session = serializers.CharField()


class VerifyEmailCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    session = serializers.CharField()


class SetPasswordSerailizer(serializers.Serializer):
    session = serializers.CharField()
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            return ValidationError({"error": _("Passwords does not match!")})

        return attrs


class PhoneNumberResetPasswordSerailizer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number', None)

        user = CustomUser.objects.filter(phone_number=phone_number)
        if not user.exists():
            raise ValidationError(
                {"phone_number": _("No user was found with this phone number")})

        data.update({'user': user.first()})
        return data


class PhoneNumberVerifyResetPasswordSertailizder(serializers.Serializer):
    phone_number = serializers.CharField()
    session = serializers.CharField()
    code = serializers.CharField()


class PhoneNumberResetPasswordSetSerailizer(serializers.Serializer):
    session = serializers.CharField()
    password = serializers.CharField(required=True)


class ProfileSerailizer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'full_name',
            'image',
            'birth_date'
        ]
