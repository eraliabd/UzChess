from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterPhoneNumberCreateView,
    RegisterEmailCreateView,
    VerifyPhoneNumberCodeView,
    VerifyEmailCodeView,
    SetPasswordView,
    PhoneNumberPasswordResetView,
    PhoneNumberresetPasswordVerifyView,
    PhoneNumberResetPasswordView,
    ProfileUserView
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('register/phone/', RegisterPhoneNumberCreateView.as_view()),
    path('register/email/', RegisterEmailCreateView.as_view()),
    path('register/phone/verify/', VerifyPhoneNumberCodeView.as_view()),
    path('register/email/verify/', VerifyEmailCodeView.as_view()),
    path('register/set_password/', SetPasswordView.as_view()),
]

urlpatterns += [
    path('phone/password/reset/', PhoneNumberPasswordResetView.as_view()),
    path('phone/password/reset/verify/',
         PhoneNumberresetPasswordVerifyView.as_view()),
    path('phone/password/reset/set/', PhoneNumberResetPasswordView.as_view()),
    path('profile/<int:pk>/', ProfileUserView.as_view())
]
