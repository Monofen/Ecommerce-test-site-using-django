# Generated by Django 4.2.14 on 2024-08-25 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_type',
            field=models.CharField(choices=[('site-wide', 'Site-wide'), ('category', 'Category')], max_length=20),
        ),
        migrations.AlterField(
            model_name='sale',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
