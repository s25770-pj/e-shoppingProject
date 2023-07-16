# Generated by Django 4.2.3 on 2023-07-16 12:35

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to=base.models.ProductImageUploadPath('base/product_images/'), validators=[base.models.validate_min_resolution]),
        ),
    ]