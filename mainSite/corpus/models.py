from django.db import models


# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=500, primary_key=True)
    user_password_hash = models.CharField(max_length=64)


class Corpus(models.Model):
    save_path = models.FilePathField(primary_key=True)
    visible = models.BooleanField(default=True)
    author = models.CharField(max_length=500)
    title = models.CharField(max_length=500, default="")
    publish_time = models.DateTimeField("essay published", auto_now=True)
    last_update_time = models.DateTimeField("essay update")
    theme_name = models.CharField(max_length=500)


class Theme(models.Model):
    theme_name = models.CharField(max_length=500, primary_key=True)
    description = models.CharField(max_length=500)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
