from django.db.models import signals
from django.dispatch import receiver

from codertheory.shiritori import models
from codertheory.shiritori.api.serializers import *
from codertheory.shiritori.events import ShiritoriEvents
from codertheory.utils.ws_utils import send_data_to_channel


