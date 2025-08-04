from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Product, File


@admin.register(Category)
class CategoyAdmin(admin.ModelAdmin):
    list_display = ['parent', 'title', 'is_enable']
    list_filter = ['is_enable', 'parent']
    search_fields = ['title']


class FileInlineAdmin(admin.StackedInline):
    model = File
    fields = ['title', 'file', 'is_enable', 'file_type']
    extra = 0


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id', 'title', 'is_enable', 'created_time']
    list_filter = ['is_enable']
    search_fields = ['title']
    filter_horizontal = ['categories']
    inlines = [FileInlineAdmin]
