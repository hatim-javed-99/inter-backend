# Generated by Django 3.2.15 on 2024-09-07 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_rename_sub_category_subcategory_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='sub_category',
        ),
    ]
