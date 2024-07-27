import requests

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from django.db import models
from django.core.cache import cache
from typing import Type
from core.utils import get_user_data, get_products_data
from django.shortcuts import get_object_or_404
from .models import (
    ProductView, ProductViewByAge, ProductViewByGender,
    ProductViewByCountry,
)
from .serializers import (
    ProductViewSerializer, ProductViewByGenderSerializer, ProductViewByAgeSerializer,
    ProductViewByCountrySerializer,
)

# TODO: GET CACHE FROM OTHER MICROSERVICE
# TODO: DO MORE BEAUTIFUL ANALYTICS BY USER_ID AND PRODUCT_ID

# TODO: 1. NEWEST PRODUCTS
# TODO: 2. MOST VIEWED PRODUCTS
# TODO: 3. TOP RATED PRODUCTS
# TODO: 4. RECOMMENDED PRODUCTS
# TODO: 5. BEST SELLER PRODUCTS
# TODO: 6. HOTTEST PRODUCTS
# TODO: 7. BY USER
# TODO: 8. BY GENDER
# TODO: 9. BY AGE
# TODO: 10. BY COUNTRY
# TODO: 11. REGISTERED USERS (WITH DELETE)
# TODO: 12. VISITED USERS (DAY, WEEK, MOTH)
class AnalyticsViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def increment_view(request, model_class: Type[models.Model], filter_field, user_field):
        product_id = request.data.get('product_id', None)
        if product_id is None:
            return Response("product_id is required", status=status.HTTP_404_NOT_FOUND)

        user_access_token = request.headers.get('Authorization', None)
        if user_access_token is None:
            return Response("user_access_token is required", status=status.HTTP_404_NOT_FOUND)

        user_data = get_user_data(user_access_token)
        user_field_value = user_data.get(user_field)

        cache_key = f"viewed_{user_field_value}_{product_id}"
        if cache.get(cache_key) is not None:
            return Response("Already viewed", status=status.HTTP_200_OK)

        view_obj, created = model_class.objects.get_or_create(
            product_id=product_id,
            **{filter_field: user_field_value},
            defaults={'count': 1}
        )
        if created is False:
            view_obj.count += 1
            view_obj.save()

        cache.set(cache_key, True, 24 * 60 * 60)
        return Response("success", status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['product_id', 'user_id'],
        ),
        responses={200: ProductViewSerializer()},
        tags=['Increment']
    )
    @action(detail=True, methods=['post'])
    def increment_product_view(self, request):
        return self.increment_view(request, ProductView, 'user_id', 'id')

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'gender': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['product_id', 'gender'],
        ),
        responses={200: ProductViewByGenderSerializer()},
        tags=['Increment']
    )
    @action(detail=True, methods=['post'])
    def increment_view_by_gender(self, request):
        return self.increment_view(request, ProductViewByGender, 'gender', 'gender')

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['product_id', 'age'],
        ),
        responses={200: ProductViewByAgeSerializer()},
        tags=['Increment']
    )
    @action(detail=True, methods=['post'])
    def increment_view_by_age(self, request):
        return self.increment_view(request, ProductViewByGender, 'gender', 'gender')

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'country': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['product_id', 'country'],
        ),
        responses={200: ProductViewByCountrySerializer()},
        tags=['Increment']
    )
    @action(detail=True, methods=['post'])
    def increment_view_by_country(self, request):
        return self.increment_view(request, ProductViewByCountry, 'country', 'country')


class AnalyticsListViewSet(ViewSet):
    # permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Get product view count by product ID",
        manual_parameters=[openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)],
        responses={200: openapi.Response(description="Successful retrieval"), 404: "Product ID not found"},
        tags=['Analytics']
    )
    @action(detail=True, methods=['get'])
    def analytics_product_view(self, request):
        product_id = request.query_params.get('product_id')
        if product_id is None:
            return Response("Product id is not found", status=status.HTTP_404_NOT_FOUND)

        analytics = ProductView.objects.filter(product_id=product_id)
        if analytics is None:
            return Response("No data found for the given product", status=status.HTTP_404_NOT_FOUND)

        serializer = {
            'product_id': product_id,
            'view_count': sum([i.view_count for i in analytics])
        }

        return Response(serializer, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Get product view analytics by user ID",
        manual_parameters=[openapi.Parameter('user_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)],
        responses={200: ProductViewSerializer(many=True)},
        tags=['Analytics']
    )
    @action(detail=True, methods=['get'])
    def analytics_product_view_by_user(self, request):
        user_id = request.query_params.get('user_id')
        if user_id is None:
            return Response("User id is not found", status=status.HTTP_404_NOT_FOUND)

        analytics = ProductView.objects.filter(user_id=user_id)
        if analytics is None:
            return Response("No data found for the given user", status=status.HTTP_404_NOT_FOUND)

        serializer = ProductViewSerializer(analytics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get most viewed products.",
        responses={200: 'List of most viewed products'},
        tags=['Analytics']
    )
    @action(detail=True, methods=['get'])
    def most_viewed_products(self, request):
        product_view_obj = ProductView.objects.all()
        count_by_id = {}

        for item in product_view_obj:
            if item.product_id in count_by_id:
                count_by_id[item.product_id] += item.view_count
            else:
                count_by_id[item.product_id] = item.view_count

        counted_products = [{'id': i, 'view_count': n} for i, n in count_by_id.items()]
        products = get_products_data()

        for product in products:
            for counted_product in counted_products:
                if product['id'] == counted_product['id']:
                    product['view_count'] = counted_product['view_count']
                else:
                    product['view_count'] = 0

        products.sort(key=lambda x: x['view_count'], reverse=True)
        return Response(products, status=status.HTTP_200_OK)
