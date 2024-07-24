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
from core.utils import get_user_data
from .models import (
    ProductView, ProductViewByAge, ProductViewByGender,
    ProductViewByCountry,
)
from .serializers import (
    ProductViewSerializer, ProductViewByGenderSerializer, ProductViewByAgeSerializer,
    ProductViewByCountrySerializer,
)


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
    )
    @action(detail=True, methods=['post'])
    def increment_view_by_country(self, request):
        return self.increment_view(request, ProductViewByCountry, 'country', 'country')
