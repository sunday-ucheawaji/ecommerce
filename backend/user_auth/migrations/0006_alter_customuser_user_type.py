# Generated by Django 4.0.7 on 2022-10-13 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0005_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('customer', 'customer'), ('supplier', 'supplier'), ('staff', 'staff')], default='customer', max_length=20),
        ),
    ]
