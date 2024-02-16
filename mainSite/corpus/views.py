import hashlib
import os
import random

from django.conf import settings
from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from spire.doc import Document
from spire.doc import FileFormat
from .models import User, Corpus, Theme
from .form import UserForm, ThemeForm, UploadForm

# Create your views here.


def doc2Html(path: str):
    document = Document()
    document.LoadFromFile(path)
    save_path = os.path.dirname(path)
    file_save_name = os.path.basename(path).split(".")[0] + ".html"
    absolute_name = os.path.join(save_path, file_save_name)
    document.SaveToFile(absolute_name, FileFormat.Html)
    document.Close()
    return absolute_name


def read_html(path):
    save_path = os.path.dirname(path)
    file_save_name = os.path.basename(path).split(".")[0] + ".html"
    absolute_name = os.path.join(save_path, file_save_name)
    with open(absolute_name, encoding="utf-8") as f:
        return f.read()


def mainSite(requestion: HttpRequest):
    if requestion.COOKIES.get("verify_code", "*") != requestion.session.get("verify_code", "**"):
        return render(request=requestion, template_name="login.html")
    user_name = eval(requestion.COOKIES.get("user_name")).decode("utf-8")
    if user_name == "ZZH_admin":
        authorize = 1
    else:
        authorize = 0
    if theme := requestion.GET.get("theme"):
        rank = 1
        articles = Corpus.objects.filter(visible=True, theme_name=theme)
    else:
        rank = 0
        articles = Theme.objects.all()
    if requestion.COOKIES.get("verify_code", "*") != requestion.session.get("verify_code", "**"):
        return render(request=requestion, template_name="login.html")
    return render(request=requestion, template_name="MainSite.html",
                  context={"articles": articles,
                           "field": "For All",
                           "authorize": authorize,
                           "rank": rank})

def createTheme(requestion: HttpRequest):
    if requestion.method == "POST":
        theme = requestion.POST.get("theme_name")
        description = requestion.POST.get("description")
        start_time = requestion.POST.get("start_time")
        end_time = requestion.POST.get("end_time")
        series = Theme(theme_name=theme, description=description, start_time=start_time, end_time=end_time)
        series.save()
        return redirect(reverse("index"))
    else:
        return render(request=requestion, template_name="Theme.html", context={"form": ThemeForm()})

def changeVisible(requestion: HttpRequest):
    if requestion.method == "GET":
        save_path = requestion.GET.get("save_path")
        article = Corpus.objects.filter(save_path=save_path)[0]
        article.visible = not article.visible
        article.save()
        redir = reverse("manage")
        return redirect(redir)


def deleteArticle(requestion: HttpRequest):
    if requestion.method == "GET":
        save_path = requestion.GET.get("save_path")
        article = Corpus.objects.filter(save_path=save_path)[0]
        article.delete()
        redir = reverse("manage")
        return redirect(redir)


def returnFile(requestion: HttpRequest):
    if requestion.method == "GET":
        file_path = requestion.GET.get("save_path")
        try:
            response = FileResponse(open(file_path, "rb"))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        except:
            return HttpResponse("Are You Kinding Me???")


def manage(requestion: HttpRequest):
    user_name = eval(requestion.COOKIES.get("user_name")).decode("utf-8")
    if requestion.COOKIES.get("verify_code", "*") != requestion.session.get("verify_code", "**"):
        return render(request=requestion, template_name="login.html")
    articles = Corpus.objects.filter(author=user_name)
    return render(request=requestion, template_name="Manage.html",
                  context={"articles": articles, "field": user_name, "authorize": 1})


def user_login(requestion: HttpRequest):
    if requestion.method == "POST":
        user_name = requestion.POST.get("user_name")
        user_password: str = requestion.POST.get("user_password", default="*")
        user = User.objects.filter(user_name=user_name)
        if not user:
            return HttpResponse("Account not exist.")
        if hashlib.sha256(user_password.encode()).hexdigest() != user[0].user_password_hash:
            return HttpResponse("password error.")
        else:
            redir = reverse("index")
            response = redirect(redir)
            verify_code = str(random.random())
            response.set_cookie(key="verify_code", value=verify_code)
            response.set_cookie(key="user_name", value=str(user_name.encode("utf-8")))
            requestion.session["verify_code"] = verify_code
            return response
    elif requestion.method == "GET":
        return render(request=requestion, template_name="login.html")


def user_logout(requestion: HttpRequest):
    if requestion.method == "GET":
        requestion.COOKIES["user_name"] = None
        return render(request=requestion, template_name="login.html")


def user_register(requestion: HttpRequest):
    if requestion.method == "POST":
        user_name = requestion.POST.get("user_name")
        if User.objects.filter(user_name=user_name):
            return HttpResponse("Author Exist!")
        user_password: str = requestion.POST.get("user_password")
        new_user = User(user_name=user_name, user_password_hash=hashlib.sha256(user_password.encode()).hexdigest())
        new_user.save()
        return render(request=requestion, template_name="login.html")
    if requestion.method == "GET":
        return render(request=requestion, template_name="register.html")


def upload(requestion: HttpRequest):
    if requestion.method == "POST":
        user_name = eval(requestion.COOKIES.get("user_name")).decode("utf-8")
        if requestion.COOKIES.get("verify_code", "*") != requestion.session.get("verify_code", "**"):
            return render(request=requestion, template_name="login.html")
        else:
            theme = requestion.POST.get("theme")
            visible = bool(requestion.POST.get("visible", True))
            title = requestion.POST.get("title")
            path = os.path.join(settings.MEDIA_ROOT, user_name)
            if not os.path.exists(path):
                os.makedirs(path)
            save_path = os.path.join(path, requestion.FILES.get("article").name)
            new_corpus = Corpus(visible=visible,
                                save_path=save_path,
                                title=title,
                                author=user_name,
                                publish_time=timezone.now(),
                                last_update_time=timezone.now(),
                                theme_name=theme)
            suffix = os.path.basename(save_path).split(".")[-1]
            if (not (files := requestion.FILES.get("article", None))) or (suffix not in {"doc", "docx"}):
                return HttpResponse("Please upload a valid file !!!!!")
            with open(save_path, "wb+") as f:
                for chunk in files.chunks():
                    f.write(chunk)
            doc2Html(path=save_path)
            new_corpus.save()
            redir = reverse("index")
            return redirect(redir)
    else:
        # now = timezone.now()
        # fesible_theme = Theme.objects.filter(start_time__lt=now, end_time__gt=now)
        fesible_theme = Theme.objects.all()
        return render(request=requestion, template_name="upload.html", context={"fesible_theme": fesible_theme})


def view_content(requestion: HttpRequest):
    if requestion.method == "GET":
        file_path = requestion.GET.get("save_path")
        title = Corpus.objects.filter(save_path=file_path)[0].title
        return render(request=requestion, template_name="view.html",
                      context={"title": title, "content": read_html(path=file_path)})

