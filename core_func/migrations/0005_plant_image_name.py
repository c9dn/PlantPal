# Generated by Django 4.2.13 on 2024-06-02 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_func', '0004_alter_plant_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='image_name',
            field=models.CharField(default='h', max_length=100),
            preserve_default=False,
        ),
    ]