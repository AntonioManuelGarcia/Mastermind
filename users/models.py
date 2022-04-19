from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(_('email address'), unique=True, db_index=True)

    is_active = models.BooleanField(_('active'), default=True, db_index=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    create_date = models.DateTimeField(_('date joined'), default=timezone.now, db_index=True, )
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)
