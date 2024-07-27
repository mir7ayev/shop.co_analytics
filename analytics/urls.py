from django.urls import path
from .views import AnalyticsViewSet, AnalyticsListViewSet

urlpatterns = [

    path('increment-product-view/', AnalyticsViewSet.as_view({'post': 'increment_product_view'})),
    path('increment-view-by-gender/', AnalyticsViewSet.as_view({'post': 'increment_view_by_gender'})),
    path('increment-view-by-age/', AnalyticsViewSet.as_view({'post': 'increment_view_by_age'})),
    path('increment-view-by-country/', AnalyticsViewSet.as_view({'post': 'increment_view_by_country'})),

    path('analytics-product-view/', AnalyticsListViewSet.as_view({'get': 'analytics_product_view'})),
    path('analytics-product-view-by-user/', AnalyticsListViewSet.as_view({'get': 'analytics_product_view_by_user'})),

    path('most-viewed-products/', AnalyticsListViewSet.as_view({'get': 'most_viewed_products'})),

]
