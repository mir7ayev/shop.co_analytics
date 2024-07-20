from django.db import models
from core.models import BaseModel


class BaseView(BaseModel):
    product_id = models.PositiveIntegerField()
    view_count = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True

    def __str__(self):
        return f'Product {self.product_id} - Views: {self.view_count}'


class ProductView(BaseView):
    user_id = models.PositiveIntegerField()

    class Meta:
        unique_together = ('product_id', 'user_id')
        verbose_name = 'Product View'
        verbose_name_plural = 'Product Views'

    def __str__(self):
        return f"Product ID: {self.product_id}, User ID: {self.user_id}, Views: {self.view_count}"


class ProductViewByGender(BaseView):
    gender = models.CharField(max_length=120)

    class Meta:
        unique_together = ('product_id', 'gender')
        verbose_name = 'Product View By Gender'
        verbose_name_plural = 'Product Views By Gender'

    def __str__(self):
        return f'Product {self.product_id} viewed by {self.gender}'


class ProductViewByAge(BaseView):
    age = models.PositiveIntegerField()

    class Meta:
        unique_together = ('product_id', 'age')
        verbose_name = 'Product View By Age'
        verbose_name_plural = 'Product Views By Age'

    def __str__(self):
        return f'Product {self.product_id} viewed by Age Group {self.age_group}'


class ProductViewByCountry(BaseView):
    country = models.CharField(max_length=120)

    class Meta:
        unique_together = ('product_id', 'country')
        verbose_name = 'Product View By Country'
        verbose_name_plural = 'Product Views By Country'

    def __str__(self):
        return f'Product {self.product_id} viewed in {self.country}'
