import uuid
from django.conf import settings
from django.utils.http import int_to_base36

def id_gen() -> str:
    """Generates random string whose length is `ID_LENGTH`"""
    return int_to_base36(uuid.uuid4().int)[:settings.DEFAULT_ID_LENGTH]