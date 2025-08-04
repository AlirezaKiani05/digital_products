
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerializer, FileSerializer, CategorySerializer
from .models import Category, Product, File
from utils.permissions import HasActiveSubscription


class ProductListView(APIView):

    def get(self, request):
        print(request.user)
        print(request.auth)
        products = Product.objects.all()
        context = {'request': request}
        serializer = ProductSerializer(products, many=True, context=context)
        return Response(serializer.data)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated,HasActiveSubscription]

    def get(self, request, pk):
        
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryDetailView(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)


# class FileListView(APIView):
#     def get(self, request, product_id):
#         files = File.objects.filter(product_id=product_id)
#         serializer = FileSerializer(
#             files, many=True, context={'request': request})
#         return Response(serializer.data)
#
# ویو قایل لیست  بالا درسته و طبق ویدیو هستش ولی کدی که این پایین زدم دقیق تره چون اگز پروداکتی وارد شه که وجود نداشته باشه
#    کد بالا جوابی برنمیگردونه ولی پایینی چهارصد و چهار میده
# ولی نشد برای دیتیل این کارو کنم
class FileListView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        files = File.objects.filter(pk=product.pk)
        serializer = FileSerializer(
            files, many=True, context={'request': request})
        return Response(serializer.data)


class FileDetailView(APIView):
    def get(self, request, product_id, pk):
        try:
            file = File.objects.get(product_id=product_id, pk=pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FileSerializer(file, context={'request': request})
        return Response(serializer.data)
