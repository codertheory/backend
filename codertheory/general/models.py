from django.db.models import Model,DateTimeField
from django.forms import model_to_dict

from codertheory.general.custom_fields import NanoIDField


class BaseModel(Model):
    id = NanoIDField()
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, BaseModel):
            return other.id == self.id
        else:
            return other == self.id

    def to_dict(self):
        return model_to_dict(self)
