from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import validate_email, RegexValidator
from django.utils.translation import gettext_lazy as _
import re


# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError('mobile must be set')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile, password, **extra_fields)


mobile_validator = RegexValidator(
    re.compile(r'^-?\d{10}\Z'),
    message=_('Enter a 10 digits mobile number.'),
    code='invalid',
)


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,
        null=True
    )
    mobile = models.CharField(
        _("mobile no"),
        unique=True,
        max_length=10,
        validators=[mobile_validator],
        help_text=_('Required. Enter your mobile number'),
        error_messages={
            'unique': _('Mobile number already registered')
        }
    )
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30, null=True, blank=True)

    email = models.EmailField(
        _('email address'),
        unique=False,
        validators=[validate_email],
        help_text=_('Required. Enter your email address'),
        error_messages={
            'unique': _("A user with same email already exists."),
        },
        null=False,
        blank=True,
    )

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = UserManager()


