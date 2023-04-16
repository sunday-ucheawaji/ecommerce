from django.urls import path
from order.views import order_views
from order.views import store_views
from order.views import cart_views


urlpatterns = [
    path("", order_views.OrderListView.as_view(), name="Order List"),
    path("<int:pk>", order_views.OrderDetailView.as_view(), name="Order Detail"),
    path("order-item", order_views.OrderItemListView.as_view(),
         name="Order Item List"),
    path("order-item/<int:pk>", order_views.OrderItemDetailView.as_view(),
         name="Order Item Detail"),
    path("store", store_views.StoreListView.as_view(),
         name="Store List"),
    path("store/<int:pk>", store_views.StoreDetailView.as_view(),
         name="Store Detail"),
    path("cart", cart_views.CartListView.as_view(),
         name="Cart List"),
    path("cart/<int:pk>", cart_views.CartDetailView.as_view(),
         name="Cart Detail"),
    path("cart-item", cart_views.CartItemListView.as_view(),
         name="Cart Item List"),
    path("cart-item/<int:pk>", cart_views.CartItemDetailView.as_view(),
         name="Cart Item Detail"),
]
