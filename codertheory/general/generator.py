import nanoid
from django.conf import settings


def generate_id():
    return nanoid.generate(size=settings.SNOWFLAKE_SIZE)
