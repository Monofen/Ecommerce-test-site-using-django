# Generated by Django 5.0.7 on 2024-08-21 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0002_alter_sellers_extra_alter_sellers_facebook_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellers',
            name='cit_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sellers',
            name='citizenship',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/owner_detail/'),
        ),
        migrations.AddField(
            model_name='sellers',
            name='owner_pic',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/owner_detail/'),
        ),
        migrations.AddField(
            model_name='sellers',
            name='pan_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sellers',
            name='pan_pic',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/owner_detail/'),
        ),
        migrations.AddField(
            model_name='sellers',
            name='registration_certificate',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/owner_detail/'),
        ),
    ]
