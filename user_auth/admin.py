from django.contrib import admin
from user_auth.models.custom_user import CustomUser
from user_auth.models.customer import Customer
from user_auth.models.staff import Staff
from user_auth.models.supplier import Supplier


admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Supplier)
