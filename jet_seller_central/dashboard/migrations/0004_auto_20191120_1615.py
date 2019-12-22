# Generated by Django 2.2.7 on 2019-11-20 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20191119_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code_type',
            field=models.CharField(choices=[('UPC', 'UPC')], max_length=100),
        ),
    ]