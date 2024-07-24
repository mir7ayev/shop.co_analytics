from rest_framework.serializers import ModelSerializer
from .models import (
    ProductView, ProductViewByGender, ProductViewByAge, ProductViewByCountry,
)


class ProductViewSerializer(ModelSerializer):
    class Meta:
        model = ProductView
        fields = ('user_id', 'product_id', 'view_count')


class ProductViewByGenderSerializer(ModelSerializer):
    class Meta:
        model = ProductViewByGender
        fields = ('product_id', 'gender', 'view_count')


class ProductViewByAgeSerializer(ModelSerializer):
    class Meta:
        model = ProductViewByAge
        fields = ('product_id', 'age', 'view_count')


class ProductViewByCountrySerializer(ModelSerializer):
    class Meta:
        model = ProductViewByCountry
        fields = ('product_id', 'country', 'view_count')
