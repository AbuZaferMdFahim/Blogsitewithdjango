# Generated by Django 4.2.1 on 2023-05-15 11:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectid', models.BigIntegerField()),
                ('text', models.CharField(max_length=150)),
                ('isseen', models.BooleanField(default=False)),
                ('notificationtypes', models.CharField(choices=[('Blog', 'Blog'), ('Llke', 'Llke'), ('Follow', 'Follow')], max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contenttype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notification', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
