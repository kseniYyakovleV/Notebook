from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django import forms
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

class form(forms.Form):
    start_datetime = forms.DateTimeField()
    

def base_view(request: HttpRequest)-> HttpResponse:
    template_name = "notebook/base.html"
    return render(request, template_name)

def new_task_view(request: HttpRequest)-> HttpResponse:
    f = form()
    context = {"datetime_form": f}
    template_name = "notebook/new_task.html"
    return render(request, template_name, context)

def add_task_view(request: HttpRequest)-> HttpResponse:
    print(request.POST)
    return redirect("/notebook/my_tasks")

def my_tasks_view(request: HttpRequest)-> HttpResponse:
    context = {
        "urgency": "Важная",
        "urgency_class": "important",
        "title": "Покормить кота",
        "time_label": "Конец",
        "deadline": "11.12.2923 23:33",
    }
    template_name = "notebook/my_tasks.html"
    return render(request, template_name, context)

def account_view(request: HttpRequest)-> HttpResponse:
    return HttpResponse("Account page")


def login_view(request: HttpRequest)-> HttpResponse:
    template_name = "notebook/login.html"
    context = {"login_form": AuthenticationForm, "is_hidden" : True}
    if request.method == "GET":
        return render(request, template_name, context)
    else:
        user = authenticate(username = request.POST["username"], password = request.POST["password"])
        if user:
            login(request, user)
        else:
            context["is_hidden"] = False
            return render(request, template_name, context)
    return redirect("/notebook/my_tasks")
    



def registration_view(request: HttpRequest)-> HttpResponse:
    context = dict()
    if request.method == "GET":
        template_name = "notebook/registration.html"
        context = {"registration_form": UserCreationForm()}
        return render(request, template_name, context)
    else:
        if UserCreationForm(request.POST).is_valid():
            context["is_valid"] = True
            if not User.objects.filter(username = request.POST["username"]).exists():
                context["is_exists"] = False
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                login(request, user)
    print(context)
    return redirect("/notebook/my_tasks")

    

def logout_view(request: HttpRequest):
    print(request.user)
    logout(request)
    return redirect("/notebook/login")

    
    