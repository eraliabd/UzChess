from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from django.core.cache import cache
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _


from .serializers import (
    RegisterUserPhoneNumberSerailzier,
    RegisterUserEmailSerailzier,
    VerifyPhoneNumberCodeSerializer,
    VerifyEmailCodeSerializer,
    SetPasswordSerailizer,
    PhoneNumberResetPasswordSerailizer,
    PhoneNumberVerifyResetPasswordSertailizder,
    PhoneNumberResetPasswordSetSerailizer,
    ProfileSerailizer
)
from .models import CustomUser
from .generators import generate_auth_session, generate_verification_code
from .message_sender import send_verification_code_email, send_verification_code_sms

# Create your views here.


class RegisterPhoneNumberCreateView(generics.GenericAPIView):
    serializer_class = RegisterUserPhoneNumberSerailzier

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        session = generate_auth_session()

        if data["auth_type"] == 'phone_number':

            phone_number = data["phone_number"]
            if cache.get(phone_number, None) is not None:
                return Response(
                    data={
                        "error": "Verification code is already sent. Please wait for a while before continue"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            code = generate_verification_code()
            send_verification_code_sms(phone_number, code)
            phone_data = {
                "session": session,
                "code": code,
            }
            cache.set(phone_number, phone_data, 120)
            data.update({"phone_number": phone_number})

        cache.set(session, data, 360)
        data.update({"session": session})
        return Response(data=data, status=status.HTTP_200_OK)


class RegisterEmailCreateView(generics.GenericAPIView):
    serializer_class = RegisterUserEmailSerailzier

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        session = generate_auth_session()

        if data["auth_type"] == 'email':

            email = data["email"]
            if cache.get(email, None) is not None:
                return Response(
                    data={
                        "error": "Verification code is already sent. Please wait for a while before continue"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            code = generate_verification_code()
            send_verification_code_email(email, code)
            email_data = {
                "session": session,
                "code": code,
            }
            cache.set(email, email_data, 120)
            data.update({"email": email})

        cache.set(session, data, 360)
        data.update({"session": session})
        return Response(data=data, status=status.HTTP_200_OK)


class VerifyPhoneNumberCodeView(generics.GenericAPIView):
    serializer_class = VerifyPhoneNumberCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        session = serializer.validated_data['session']
        code = serializer.validated_data['code']

        cache_data = cache.get(phone_number, None)

        if cache_data is None:
            # if nothing is found with given phone number or email
            return Response(
                data={"error": _(
                    "Verification code is expired. Or invalid phone entered!")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if cache_data["code"] != code:
            # if incorrect code is entered
            return Response(data={"error": _("Incorrect Code!")})

        session_cache_data = cache.get(session, None)
        session_cache_data.update({"is_verified": True})
        cache.set(session, session_cache_data)

        return Response(data={"message": _("Your verification completed successfully!")}, status=status.HTTP_200_OK)


class VerifyEmailCodeView(generics.GenericAPIView):
    serializer_class = VerifyEmailCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        session = serializer.validated_data['session']
        code = serializer.validated_data['code']

        cache_data = cache.get(email, None)

        if cache_data is None:
            # if nothing is found with given phone number or email
            return Response(
                data={"error": _(
                    "Verification code is expired. Or invalid phone entered!")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if cache_data["code"] != code:
            # if incorrect code is entered
            return Response(data={"error": _("Incorrect Code!")})

        session_cache_data = cache.get(session, None)
        session_cache_data.update({"is_verified": True})
        cache.set(session, session_cache_data)

        return Response(data={"message": _("Your verification completed successfully!")}, status=status.HTTP_200_OK)


class SetPasswordView(generics.GenericAPIView):
    serializer_class = SetPasswordSerailizer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = serializer.validated_data['session']
        password = serializer.validated_data['password']

        session_data = cache.get(session, None)

        if session_data is None:
            return Response({'error': "Invalid session!"})

        is_verified = session_data.pop("is_verified", None)
        if is_verified is None:
            return Response(
                data={"error": _("User is not verified with this session!")}, status=status.HTTP_400_BAD_REQUEST
            )

        user = CustomUser(**session_data)
        user.set_password(password)
        user.save()

        # session_data.update(user.get_tokens())

        return Response(session_data, status=status.HTTP_201_CREATED)


class PhoneNumberPasswordResetView(generics.GenericAPIView):
    serializer_class = PhoneNumberResetPasswordSerailizer

    def post(self, request):
        serailizer = self.get_serializer(data=request.data)
        serailizer.is_valid(raise_exception=True)

        phone_number = serailizer.validated_data['phone_number']
        user = serailizer.validated_data['user']

        if cache.get(phone_number, None) is not None:
            return Response(
                data={"error": _(
                    "Code is already sent. Please, wait a while before continue")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = generate_auth_session()
        code = generate_verification_code()

        # cache.set(session, code, 120)

        send_verification_code_sms(phone_number=phone_number, code=code)

        phone_number_data = {
            'session': session,
            'code': code
        }

        cache.set(phone_number, phone_number_data, 120)
        cache.set(session, {'user_id': user.id}, 600)

        return Response(data={'session': session}, status=status.HTTP_200_OK)


class PhoneNumberresetPasswordVerifyView(generics.GenericAPIView):
    serializer_class = PhoneNumberVerifyResetPasswordSertailizder

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        session = serializer.validated_data['session']
        code = serializer.validated_data['code']

        cache_data = cache.get(phone_number, None)

        if cache_data is None:
            return Response(
                data={"error": _(
                    "Code is expired or Incorrect phone number was entered")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if code != cache_data['code']:
            return Response(data={'error': "Incorrect Code"}, status=status.HTTP_400_BAD_REQUEST)

        session_data = cache.get(session, None)
        session_data.update({'is_verify': True})
        cache.set(session, session_data, 600)

        # print(cache.get(session))

        return Response(
            data={
                "message": _("Confirmed successfully!"),
                'session': _(session)
            },
            status=status.HTTP_200_OK
        )


class PhoneNumberResetPasswordView(generics.GenericAPIView):
    serializer_class = PhoneNumberResetPasswordSetSerailizer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = serializer.validated_data['session']
        password = serializer.validated_data['password']

        session_data = cache.get(session)

        if not session_data['is_verify']:
            return Response(
                data={
                    'error': "Not Confirmed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(
            CustomUser.objects.all(), id=session_data['user_id'])
        user.set_password(password)
        user.save()

        return Response(
            data={
                'message': _("Successfully changed")
            },
            status=status.HTTP_200_OK
        )



class ProfileUserView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerailizer