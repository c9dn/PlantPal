# Generated by Django 4.2.13 on 2024-06-02 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_email_provider'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='community',
            new_name='community_name',
        ),
    ]
