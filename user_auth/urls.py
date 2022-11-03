from django.urls import path
from user_auth.views import custom_user_views
from user_auth.views import customer_view
from user_auth.views import supplier_view
from user_auth.views import staff_view

urlpatterns = [
    path("", custom_user_views.UserListView.as_view(), name="all_users"),
    path("<int:pk>", custom_user_views.UserDetailView.as_view(), name="user"),

    path("register", custom_user_views.RegisterView.as_view(), name="register"),
    path("login", custom_user_views.LoginView.as_view(), name="login"),
    path("logout", custom_user_views.logout_view, name="logout"),

    path("customers/", customer_view.RegisterCustomerView.as_view(),
         name="customer list"),
    path("customers/<int:pk>", customer_view.CustomerDetailView.as_view(),
         name="customer detail"),

    path("suppliers/", supplier_view.SupplierListView.as_view(), name="supplier list"),
    path("suppliers/<int:pk>", supplier_view.SupplierDetailView.as_view(),
         name="supplier detail"),

    path("staff/", staff_view.StaffListView.as_view(), name="staff list"),
    path("staff/<int:pk>", staff_view.StaffDetailView.as_view(),
         name="staff detail"),
    path("multiple", custom_user_views.CreateMultipleUsers.as_view(), name="multiple"),
    path("delete", custom_user_views.DeleteUserView.as_view(), name="delete")

]
