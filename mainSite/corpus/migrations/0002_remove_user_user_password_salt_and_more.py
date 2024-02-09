# Generated by Django 5.0.1 on 2024-02-04 18:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('corpus', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_password_salt',
        ),
        migrations.AddField(
            model_name='user',
            name='user_password_hash',
            field=models.CharField(default='*', max_length=64),
            preserve_default=False,
        ),
    ]