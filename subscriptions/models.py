from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.validators import sku_validator


class Package(models.Model):
    title = models.CharField(_('title'), max_length=20)
    sku = models.CharField(_('stock keeping unit'), max_length=20, validators=[
                           sku_validator], db_index=True)
    description = models.TextField(_('description'), max_length=20, blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='packages/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    price = models.PositiveIntegerField(_('price'))
    duration = models.DurationField(_('duration'), blank=True, null=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('update'), auto_now=True)

    class Meta:
        db_table = 'packages'
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        'users.User', related_name='subscriptions', on_delete=models.CASCADE)
    package = models.ForeignKey(
        'Package', related_name='subscriptions', on_delete=models.CASCADE)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    expired_time = models.DateTimeField(
        _('expire time'), null=True, blank=True)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscripion'
        verbose_name_plural = 'Subscriptions'
