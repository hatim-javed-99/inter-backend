# Generated by Django 3.2.15 on 2024-09-06 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20240906_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='supplier',
        ),
        migrations.AddField(
            model_name='category',
            name='supplier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='service.supplier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcategory',
            name='sub_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='service.category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='service.subcategory'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=256),
        ),
    ]
