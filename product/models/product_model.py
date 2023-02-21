from django.db import models
from user_auth.models.custom_user import CustomUser
from product.models.category import Category, Brand


def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.supplier.id, filename)


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    model_year = models.DateField()
    list_price = models.IntegerField()
    product_image = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True)

    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=False, blank=False, related_name="products")
    category = models.ForeignKey(
        Category, null=False, blank=False, on_delete=models.CASCADE, related_name="products")
    supplier = models.ForeignKey(
        CustomUser, null=False, blank=False, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.product_name
