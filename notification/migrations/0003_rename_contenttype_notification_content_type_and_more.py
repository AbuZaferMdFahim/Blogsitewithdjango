# Generated by Django 4.2 on 2023-05-16 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_alter_notification_notificationtypes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='contenttype',
            new_name='content_type',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='isseen',
            new_name='is_seen',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='notificationtypes',
            new_name='notification_types',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='objectid',
            new_name='object_id',
        ),
    ]