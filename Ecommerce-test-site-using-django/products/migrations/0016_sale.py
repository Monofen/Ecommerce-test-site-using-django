# Generated by Django 4.2.14 on 2024-08-25 07:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_alter_product_on_sale_alter_product_sale_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_type', models.CharField(choices=[('sitewide', 'Site-wide'), ('category', 'Category')], default='sitewide', max_length=10)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
    ]
