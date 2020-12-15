import io

from django.utils.deconstruct import deconstructible
from storages.backends import sftpstorage


@deconstructible
class CustomSFTPStorage(sftpstorage.SFTPStorage):

    def _open(self, name, mode='rb'):
        return CustomSFTPStorageFile(name, self, mode)


class CustomSFTPStorageFile(sftpstorage.SFTPStorageFile):

    def write(self, content):
        if 'w' not in self.mode and "a" not in self.mode:
            raise AttributeError("File was opened for read-only access.")
        self.file = io.BytesIO(content)
        self._is_dirty = True
        self._is_read = True
