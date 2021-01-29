from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AnonymousUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from codertheory.utils.custom_fields import NanoIDField


class CustomUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        return super(CustomUserManager, self).create_superuser(None, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    id = NanoIDField()
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    role = models.CharField(_("User's Role"), max_length=75, blank=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    avatar = models.ImageField(null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into the admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if all((self.first_name, self.last_name)):
            return f"{self.first_name} {self.last_name}"
        elif self.name:
            return self.name
        else:
            return self.email

    class Meta:
        db_table = "user"

    def is_publisher(self) -> bool:
        if not isinstance(self, AnonymousUser):
            self.has_perms("")
        else:
            return False

    def get_absolute_url(self):
        return f"/users/{self.email}/"
