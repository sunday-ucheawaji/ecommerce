from django.urls import path
from order.views import order_views
from order.views import store_views


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
         name="Store Detail")
]
