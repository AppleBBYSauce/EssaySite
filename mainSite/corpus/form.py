# Item's name: form
# Autor: bby
# DateL 2024/2/9 0:07
from django.forms import ModelForm, Form
from django.forms import DateField, CharField, Textarea
from django import forms
from .models import User, Corpus, Theme

class UserForm(ModelForm):
    
    class Meta:
        model = User
        fields = "__all__"
        labels = {
            "user_name": "user name",
            "user_password_hash": "password",
        }


class UploadForm(ModelForm):

    class Meta:
        model = Corpus
        fields = ("title", "theme_name", "visible")
        labels = {
            "visible": "Determine whether to display this article to the public",
            "series_name": "Select the theme to which the article belongs",
            "title": "The title of the aritcle",
        }

class ThemeForm(Form):

    start_time = DateField(help_text="The start time of this theme", widget=forms.DateInput(attrs={"type":"date"}))
    end_time = DateField(help_text="The deadline of this theme", widget=forms.DateInput(attrs={"type":"date"}))
    theme_name = CharField(help_text="Theme Name")
    description = CharField(widget=forms.Textarea)


