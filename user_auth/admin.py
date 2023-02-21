from django.contrib import admin
from user_auth.models.custom_user import CustomUser
from user_auth.models.staff import Staff


admin.site.register(CustomUser)
admin.site.register(Staff)
