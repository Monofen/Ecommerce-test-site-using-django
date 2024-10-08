# Generated by Django 5.0.7 on 2024-08-01 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_rating_photo_alter_rating_stars'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='photo',
        ),
        migrations.AddField(
            model_name='rating',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='rating_images/'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='stars',
            field=models.PositiveIntegerField(),
        ),
    ]
