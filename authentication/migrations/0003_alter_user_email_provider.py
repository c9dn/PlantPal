# Generated by Django 4.2.13 on 2024-06-02 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_user_phone_number_user_email_user_email_core_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_provider',
            field=models.CharField(max_length=100),
        ),
    ]