# Generated by Django 4.2.3 on 2023-08-03 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_seller', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='prp_price',
            new_name='pro_price',
        ),
    ]