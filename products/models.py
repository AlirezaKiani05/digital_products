
from django.db import models

from django.utils.translation import gettext_lazy as _


class Category(models.Model):

    title = models.CharField(_('Name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(
        _('avatar'), blank=True, upload_to='categories/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created_time'), auto_now_add=True)
    updated_time = models.DateField(_('updated_time'), auto_now=True)
    parent = models.ForeignKey('self', verbose_name=_(
        'parent'), blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(_('Name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='products/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    categories = models.ManyToManyField(
        'Category', verbose_name=_('categoties'), blank=True)
    created_time = models.DateTimeField(_('created_time'), auto_now_add=True)
    updated_time = models.DateField(_('updated_time'), auto_now=True)

    class Meta:
        db_table = "products"
        verbose_name = 'product'
        verbose_name_plural = 'products'


class File(models.Model):
    FILE_AUDIO = 1
    FILE_VIDEO = 2
    FILE_PDF = 3
    FILE_TYPES = (
        (FILE_AUDIO, _('audio')),
        (FILE_VIDEO, _('video')),
        (FILE_PDF, _('pdf'))
    )
    product = models.ForeignKey('Product', verbose_name=_(
        'Product'), related_name='files', on_delete=models.CASCADE)
    title = models.CharField(max_length=20, verbose_name=_('Name'))
    file_type = models.PositiveSmallIntegerField(
        _('file_type'), choices=FILE_TYPES)
    file = models.FileField(upload_to="files/%Y/%m/%d/",
                            verbose_name=_('file'))
    is_enable = models.BooleanField(default=True, verbose_name=_('is_enable'))
    created_time = models.DateTimeField(_('created_time'), auto_now_add=True)
    updated_time = models.DateField(_('updated_time'), auto_now=True)

    class Meta:
        db_table = 'Files'
        verbose_name = 'File'
        verbose_name_plural = 'Files'
