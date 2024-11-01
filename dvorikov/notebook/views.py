from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
import pytz
import string

views.PasswordChangeView()


from .models import Task, Period

def is_title_valid(title: str)->bool:
    return title and title[0].lower() in (string.punctuation + string.whitespace + string.digits)


def create_task_from_request(request: HttpRequest)-> int:
    print(request.POST)
    title = request.POST["title"]
    category = request.POST["category"]

    start_datetime = datetime.fromisoformat(request.POST["start_time"]).replace(tzinfo=pytz.timezone("UTC")) - timedelta(0, 0, 0, 0, 0, 3, 0)
    end_datetime = datetime.fromisoformat(request.POST["end_time"]).replace(tzinfo=pytz.timezone("UTC")) - timedelta(0, 0, 0, 0, 0, 3, 0)

    is_periodic = "is_periodic" in request.POST and (request.POST["is_periodic"] == "on" or request.POST["is_periodic"] == "True" )
    task_description = request.POST["description"]
    period = request.POST["period"]
    duration = request.POST["duration"]
    task = Task.objects.create(owner = request.user,
                            title = title,
                            category = category,
                            start_datetime = start_datetime,
                            end_datetime = end_datetime,
                            task_description = task_description,
                            is_periodic = is_periodic,
                            last_execution = None,
                            )
    
    if is_periodic:
        period = Period.objects.create(task = task,
                                period_duration = period,
                                execution_duration = duration,)
        
    return task.id


    

def test_view(request: HttpRequest)-> HttpResponse:
    return JsonResponse(data={"name": request.user.username})
    return HttpResponse(request.POST)

def base_view(request: HttpRequest)-> HttpResponse:
    template_name = "notebook/base.html"
    return render(request, template_name)


def str_datetime_to_datetime(str_datetime: str, tz: timezone.tzinfo)->datetime:
    str_date, str_time = str_datetime.split('T')
    year, month, day = map(int, str_date.split('-'))
    hour, minute = map(int, str_time.split(':'))
    return datetime(year, month, day, hour, minute, 0, 0, pytz.timezone("UTC"))

@login_required
def new_task_view(request: HttpRequest)-> HttpResponse:
    "View for creating new task"
    if request.method == "GET":
        context = {"execution_duration": 1, "period_duration": 1}
        template_name = "notebook/new_task.html"
        return render(request, template_name, context)
    else :
        create_task_from_request(request)
        return redirect("/notebook/my_tasks")

@login_required
def my_tasks_view(request: HttpRequest)-> HttpResponse:
    "View for displaing all user tasks "
    tasks = map(Task.get_short_info, Task.objects.filter(owner = request.user))
    context = {"tasks": tasks}
    template_name = "notebook/my_tasks.html"
    return render(request, template_name, context)


@login_required
def task_view(request: HttpRequest, task_id: int)-> HttpResponse:
    if Task.objects.filter(owner = request.user, id = task_id).exists():
        template_name = "notebook/show_task.html"
        task = Task.objects.get(owner = request.user, id = task_id)
        context = {
            "task": task, 
            "readonly": True, 
            }
        context["status"] = context["task"].get_short_info()["status"]
        if task.is_periodic:
            period = Period.objects.get(task = context["task"])
            context["execution_duration"] = period.execution_duration
            context["period_duration"] = period.period_duration
            context["can_be_completed"] = context["status"] == "failed" or context["status"] == "current"
        else:
            context["can_be_completed"] = context["status"] == "current"
            context["execution_duration"] = context["period_duration"] = 1
        context["task"].start_datetime = (context["task"].start_datetime + timedelta(0, 0, 0, 0, 0, 3, 0)).isoformat()[:19]
        context["task"].end_datetime = (context["task"].end_datetime + timedelta(0, 0, 0, 0, 0, 3, 0)).isoformat()[:19]

        return render(request, template_name, context)
    return HttpResponseNotFound()

@login_required
def complete_view(request: HttpRequest, task_id: int)-> HttpResponse:
    if Task.objects.filter(owner = request.user, id = task_id).exists():
        Task.objects.get(owner = request.user, id = task_id).complete()
        return redirect("/notebook/my_tasks")
    return HttpResponseNotFound()


@login_required
def not_complete_view(request: HttpRequest, task_id: int)-> HttpResponse:
    if Task.objects.filter(owner = request.user, id = task_id).exists():
        Task.objects.get(owner = request.user, id = task_id).not_complete()
        return redirect("/notebook/my_tasks")
    return HttpResponseNotFound()


@login_required
def change_view(request: HttpRequest, task_id: int)-> HttpResponse:
    if Task.objects.filter(owner = request.user, id = task_id).exists():
        task = Task.objects.filter(owner = request.user, id = task_id)
        title = request.POST["title"]
        category = request.POST["category"]
        start_datetime = datetime.fromisoformat(request.POST["start_time"]).replace(tzinfo=pytz.timezone("UTC")) - timedelta(0, 0, 0, 0, 0, 3, 0)
        end_datetime = datetime.fromisoformat(request.POST["end_time"]).replace(tzinfo=pytz.timezone("UTC")) - timedelta(0, 0, 0, 0, 0, 3, 0)
        is_periodic = "is_periodic" in request.POST and (request.POST["is_periodic"] == "on" or request.POST["is_periodic"] == "True" )
        task_description = request.POST["description"]
        period_duration = request.POST["period"]
        execution_duration = request.POST["duration"]
        task.update(title = title,
                    category = category,
                    start_datetime = start_datetime,
                    end_datetime = end_datetime,
                    task_description = task_description,
                    is_periodic = is_periodic,
                    last_execution = None,
                    )
    
        task = Task.objects.get(owner = request.user, id = task_id)
        if is_periodic and task.is_periodic:
            period = Period.objects.get(task = task)
            if period.period_duration != int(period_duration) or period.execution_duration != int(execution_duration):
                Period.objects.filter(task = task).update(period_duration = period_duration, execution_duration = execution_duration, execution_count = 0)
        elif is_periodic:
            Period.objects.create(task = task, period_duration = period_duration, execution_duration = execution_duration)
        elif task.is_periodic:
            Period.objects.filter(task = task).delete()

        return redirect(f"/notebook/task/{task_id}")
    return HttpResponseNotFound

@login_required
def delete_view(request: HttpRequest, task_id: int)-> HttpResponse:
    if Task.objects.filter(owner = request.user, id = task_id).exists():
        Task.objects.get(owner = request.user, id = task_id).delete()
        return redirect("/notebook/my_tasks")
    return HttpResponseNotFound

@login_required
def account_view(request: HttpRequest)-> HttpResponse:
    template_name = "notebook/account.html"
    context = {"form": PasswordChangeForm, "name": "name"}

    return render(request, template_name, context)



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
                return redirect("/notebook/my_tasks")

    return redirect("/notebook/registration")

@login_required
def change_password_view(request: HttpRequest)->HttpResponse:
    template_name = "notebook/account.html"
    context = {"form_name": "change_password"}
    user = authenticate(username = request.user.username, password = request.POST["new_password1"])
    if user and request.POST["new_password1"] == request.POST["new_password2"]:
        request.user.set_password(request.POST["new_password1"])
        context["password_successfully_chainged"] = True
    else:
        context["wrong_password_np"] = True

    return render(request, template_name, context)

@login_required
def change_username_view(request: HttpRequest)->HttpResponse:
    template_name = "notebook/account.html"
    context = {"form_name": "change_username"}
    print(request.POST)
    user = authenticate(username = request.user.username, password = request.POST["password"])
    if user:
        request.user.username = request.POST["new_username"]
        context["username_successfully_chainged"] = True
        
    return render(request, template_name, context)


@login_required
def delete_account_view(request: HttpRequest)->HttpResponse:
    
    user = authenticate(username = request.user.username, password = request.POST["password"])
    print(request.user.username, request.POST["password"])
    if user:
        logout(request)
        user.delete()
        print("first_end")
        return redirect("/notebook/registration/")
    else:
        template_name = "notebook/account.html"
        context = {
            "wrong_password_da": True,
            "form_name": "delete_account"
        }
        print("second_end")
        return render(request, template_name, context)


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("/notebook/login")

    
    