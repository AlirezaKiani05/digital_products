
import random
import time
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager, UserManager)
from django.core.mail import send_mail
from django.core import validators




class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, phone_number=phone_number,
                          is_staff=is_staff, is_superuser=is_superuser, is_active=True, email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            elif phone_number:
                username = random.choice(
                    'qwertyuiopasdfghjklzxcvbnm')+str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))
        return self._create_user(username, phone_number, email, password, False, False, ** extra_fields)

    def create_superuser(self, username, phone_number, email, password, **extra_fields):
        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'),max_length=16, unique=True,
                                help_text=_(
        'Required 30 characters or fewer starting with a letter'),
        validators=[
        validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                                  _('Enter a valid username starting with a-z.'
                                    'this value may contain only letters,numbers,...'))
    ],
        error_messages={'unique': _(
            'A user with that username already exists')}


    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(
        _('email address'), unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(_('phone number'), unique=True, blank=True, null=True,
                                          validators=[
        validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                  _('Enter avild mobile number')
                                  )
    ],
        error_messages={'unique': _('A user with thid mobile already exist.')}
    )
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(_('last seen date'), null=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = ' custom_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_loggedin_user(self):
        return self.phone_number is not None or self.email is not None

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(_('nick_name'), max_length=32, blank=True)
    avatar = models.ImageField(
        _('avatar'), blank=True, upload_to='Userprofiles.avatar/')
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    gender = models.BooleanField(
        _("gender"), null=True, help_text='femail=False, mail=True,not_set=Null')
    province = models.ForeignKey(verbose_name=_(
        'province'), to='Province', blank=True, null=True, on_delete=models.SET_NULL)


class Meta:
    db_table = 'user_profiles'
    verbose_name = 'user_profile'
    verbose_name_plural = 'user_profiles'


@property
def get_first_name(self):
    return self.user.first_name


@property
def get_last_name(self):
    return self.user.last_name


def get_nick_name(self):
    return self.nick_name if self.nick_name else self.user.username


class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE = ((WEB, _('web')),
                   (IOS, _('ios')),
                   (ANDROID, _('android')),
                   )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='devices')
    device_uuid = models.UUIDField(_('Device UUID'), null=True)
    # notify_token = models.CharField(_('Notification token'), max_length=200,
    #             validators=[validators.RegexValidator(r'([a-z]|[A-Z]|[0-9])\w+', _('notify token is not valid'), 'invalid')])

    last_login = models.DateTimeField(_('Device lastlogin'), null=True)
    device_type = models.PositiveSmallIntegerField(
        choices=DEVICE_TYPE, default=1)
    device_os = models.CharField(_('device os'), max_length=30, blank=True)
    device_model = models.CharField(
        _('device models'), max_length=20, blank=True)
    app_version = models.CharField(_('app version'), max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_devices'
        verbose_name = 'user_device'
        verbose_name_plural = 'user_devices'
        unique_together = ('user', 'device_uuid')


class Province(models.Model):
    name = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True, auto_created=True)

    def __str__(self):
        return self.name
