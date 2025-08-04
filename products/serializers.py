
from rest_framework import serializers

from .models import File, Product, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'description', 'avatar', 'url']


class FileSerializer(serializers.ModelSerializer):
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'title', 'file', 'file_type']

    def get_file_type(self, obj):
        return obj.get_file_type_display()


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True)
    # files = FileSerializer(many=True)
    foo = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','title', 'description', 'categories', 'foo', 'url']

    def get_foo(self, obj):
        return 'از ما خرید کنید'
