def send_sms(phone_number, message):
    print(f"\nSMS sender:\n{message}\n\n")


def send_verification_code_sms(phone_number, code):
    message = f"Your verification code: {code}"
    send_sms(phone_number, message)


def send_email(email, message):
    print(f"\nEmail sender:\n{message}\n\n")


def send_verification_code_email(email, code):
    message = f"Your verification code: {code}"
    send_sms(email, message)
