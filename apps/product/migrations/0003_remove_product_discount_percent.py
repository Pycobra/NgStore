# Generated by Django 3.2.8 on 2022-02-10 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_discount_p'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount_percent',
        ),
    ]