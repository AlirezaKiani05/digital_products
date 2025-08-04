from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.validators import phone_number_validator



class Gateway(models.Model):
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), max_length=30, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='gateways/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    # credentials=models.TextField(_('credentials'),blank=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('update'), auto_now=True)

    class Meta:
        db_table = 'gateways'
        verbose_name = 'Gateway'
        verbose_name_plural = 'Gateways'


class Payment(models.Model):
    STATUS_VOID = 0
    STATUS_PAID = 10
    STATUS_ERROR = 20
    STATUS_CANCELED = 30
    STATUS_REFUNDED = 31
    STATUS_CHOICES = (
        (STATUS_VOID, _('void')),
        (STATUS_PAID, _('paid')),
        (STATUS_ERROR, _('error')),
        (STATUS_CANCELED, _('canceled')),
        (STATUS_REFUNDED, _('refunded')),
    )
    STATUS_TRANSLATIONS = {
        STATUS_VOID: 'payment could not be proccessed!',
        STATUS_PAID: 'payment successful',
        STATUS_ERROR: 'payment has error',
        STATUS_CANCELED: 'payment has been canceled by user',
        STATUS_REFUNDED: 'payment has refunded'
    }

    user = models.ForeignKey('users.User', verbose_name='user',
                             related_name='payments', on_delete=models.CASCADE)
    gateway = models.ForeignKey(
        Gateway, verbose_name='gateway', related_name='payments', on_delete=models.CASCADE)
    package = models.ForeignKey('subscriptions.Package', verbose_name='package',
                                related_name='payments', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(_('price'), default=0)
    status = models.PositiveBigIntegerField(
        _('status'), choices=STATUS_CHOICES, default=STATUS_VOID, db_index=True)
    device_uuid = models.CharField(_('device_uuid'), blank=True, max_length=40)
    phone_number = models.PositiveBigIntegerField(
        _('phone_number'), validators=[phone_number_validator], db_index=True)
    consumed_code = models.PositiveIntegerField(
        _('consumed refrence code'), null=True, db_index=True)
    token = models.CharField(_('token'),max_length=30)
    created_time = models.DateTimeField('created time', auto_now_add=True)
    update_time = models.DateTimeField('update', auto_now=True)

    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
