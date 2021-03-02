from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from ..custom_user_manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    last_name = models.CharField(
        _('first name'), max_length=50, blank=True, null=True)
    first_name = models.CharField(
        _('last name'), max_length=50, blank=True, null=True)
    address_line_1 = models.CharField(
        _('adresse line one'), max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(
        _('adresse line two'), max_length=255, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    city = models.CharField(_('city'), max_length=50, blank=True, null=True)

    email = models.EmailField(_('email address'), max_length=255, unique=True)
    phone_number = models.CharField(_('phone_number'), max_length=10,
                                    validators=[MinLengthValidator(10)])
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = CustomUserManager()

    class Meta:
        app_label = 'api'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [
                  self.email], **kwargs, fail_silently=False)

