from django.contrib import admin
from .models import (
    ProductView, ProductViewByGender, ProductViewByAge,
    ProductViewByCountry,
)


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'product_id', 'view_count')
    list_display_links = ('id', 'user_id')
    list_filter = ('product_id', 'user_id', 'view_count')
    search_fields = ('product_id', 'user_id', 'view_count')


@admin.register(ProductViewByGender)
class ProductViewByGenderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'gender', 'view_count')
    list_display_links = ('id', 'product_id')
    list_filter = ('product_id', 'gender', 'view_count')
    search_fields = ('product_id', 'gender', 'view_count')


@admin.register(ProductViewByAge)
class ProductViewByAgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'age', 'view_count')
    list_display_links = ('id', 'product_id')
    list_filter = ('product_id', 'age', 'view_count')
    search_fields = ('product_id', 'age', 'view_count')


@admin.register(ProductViewByCountry)
class ProductViewByCountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'country', 'view_count')
    list_display_links = ('id', 'product_id')
    list_filter = ('product_id', 'country', 'view_count')
    search_fields = ('product_id', 'country', 'view_count')
