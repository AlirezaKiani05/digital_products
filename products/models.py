from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=_(
        'parent'), blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('Name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(
        _('avatar'), blank=True, upload_to='categories/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created_time'), auto_now_add=True)
    updated_time = models.DateField(_('updated_time'), auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    categories = models.ManyToManyField('Category', verbose_name=_(
        "categories"), blank=True)
    title = models.CharField(verbose_name=_('Name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='products/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created_time'), auto_now_add=True)
    updated_time = models.DateField(_('updated_time'), auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'


class File(models.Model):
    product = models.ForeignKey("Product", verbose_name=_(
        "Product"), blank=True, on_delete=models.CASCADE)
    title = models.CharField(_('Name'), max_length=20)
    file = models.FileField(_('file'), upload_to='files/%Y/%m/%d/')
    is_enable = models.BooleanField(_("is_enable"), default=True)
    created_time = models.DateTimeField(_("created_time"), auto_now_add=True)
    updated_time = models.DateField(_("updated_time"), auto_now=True)

    class Meta:
        db_table = 'Files'
        verbose_name = 'File'
        verbose_name_plural = 'Files'
