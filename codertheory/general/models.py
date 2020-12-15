from django.db import models

from codertheory.utils.custom_fields import NanoIDField


class BaseModel(models.Model):
    id = NanoIDField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, BaseModel):
            return other.id == self.id
        else:
            return other == self.id
