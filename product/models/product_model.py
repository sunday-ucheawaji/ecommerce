from django.db import models
from user_auth.models.supplier import Supplier
from product.models.category import Category, Brand



def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.supplier.custom_user.id, filename)
class Product(models.Model):
    product_name = models.CharField(max_length=30)
    model_year = models.DateField()
    list_price = models.IntegerField()
    product_image = models.ImageField(upload_to = user_directory_path, blank=True, null=True)

    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.product_name
