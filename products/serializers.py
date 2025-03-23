from pyexpat import model
from rest_framework import serializers

from .models import Product, File, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'avatar', 'is_enable']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model=File
        fields=['file','title','created_time']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories=CategorySerializer(many=True)
    files=FileSerializer(many=True)
    class Meta: 
        model = Product
        fields = ['id','title', 'description','is_enable', 'categories', 'created_time','files','url']
