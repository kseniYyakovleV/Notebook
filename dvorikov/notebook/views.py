from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django import forms


class form(forms.Form):
    start_datetime = forms.DateTimeField()


# Create your views here.

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
    return HttpResponse("Список пока пуст")

def account_view(request: HttpRequest)-> HttpResponse:
    return HttpResponse("Account page")