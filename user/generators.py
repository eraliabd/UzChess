import random

from django.core.cache import cache
from django.utils.crypto import get_random_string


def generate_auth_session():
    session = get_random_string(length=32)

    while cache.get(session, None) is not None:
        session = get_random_string(length=32)

    return session


def generate_verification_code():
    code = "".join([str(random.randint(0, 100) % 10) for _ in range(6)])
    return code