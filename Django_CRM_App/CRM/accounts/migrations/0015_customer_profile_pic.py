# Generated by Django 4.2.3 on 2023-08-25 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
