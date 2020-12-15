from django.conf import settings
from django.db import models

from codertheory.utils.generator import generate_id


class NanoIDField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['default'] = generate_id
        kwargs['primary_key'] = True
        kwargs['auto_created'] = True
        kwargs['editable'] = False
        kwargs['max_length'] = settings.SNOWFLAKE_SIZE
        super().__init__(*args, **kwargs)
