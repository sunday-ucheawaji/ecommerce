from django.urls import path
from product.views import product_views
from product.views import category_views
from product.views import brand_views
from product.views import stock_views
from product.views import review


urlpatterns = [
    path("", product_views.ProductListView.as_view(), name="Product List"),
    path("<int:pk>", product_views.ProductDetailView.as_view(),
         name="Product List"),
    path("category", category_views.CategoryListView.as_view(), name="Category List"),
    path("category/<int:pk>", category_views.CategoryDetailView.as_view(),
         name="Category List"),
    path("brand", brand_views.BrandListView.as_view(), name="Brand List"),
    path("brand/<int:pk>", brand_views.BrandDetailView.as_view(),
         name="Brand List"),
    path("stock", stock_views.StockListView.as_view(), name="stock-list"),
    path("stock/<int:pk>", stock_views.StockDetailView.as_view(),
         name="stock-detail"),
    path("review", review.ReviewListView.as_view(), name="review-list"),
    path("review/<int:pk>", review.ReviewDetailView.as_view(),
         name="review-detail"),
]
