# Generated by Django 5.0.1 on 2024-02-08 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0005_alter_corpus_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('Series_name', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='corpus',
            name='publish_time',
            field=models.DateTimeField(auto_now=True, verbose_name='essay published'),
        ),
    ]
