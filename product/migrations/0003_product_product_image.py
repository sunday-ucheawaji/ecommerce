# Generated by Django 4.0.7 on 2022-11-09 20:49

from django.db import migrations, models
import product.models.product_model


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.product_model.user_directory_path),
        ),
    ]
