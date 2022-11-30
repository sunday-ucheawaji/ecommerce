from django.urls import path
from user_auth.views import custom_user_views
from user_auth.views import customer_view
from user_auth.views import supplier_view
from user_auth.views import staff_view
from user_auth.views import auth_view


urlpatterns = [
    path("", custom_user_views.UserListView.as_view(), name="all_users"),
    path("<int:pk>", custom_user_views.UserDetailView.as_view(), name="user"),

    path("register", auth_view.RegisterView.as_view(), name="register"),
    path("verify", auth_view.VerifyView.as_view(), name="verify"),

    path("forgot-password", auth_view.ForgotPasswordView.as_view(),
         name="forgot-password"),
    path("reset-password", auth_view.ResetPasswordView.as_view(),
         name="reset-password"),
    path("change-password", auth_view.ChangePasswordView.as_view(),
         name="change-password"),


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



    path("multiple", auth_view.CreateMultipleUsers.as_view(), name="multiple"),
    path("delete", auth_view.DeleteUserView.as_view(), name="delete")

]
