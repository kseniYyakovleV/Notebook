from django.urls import path
from .views import *

urlpatterns = [
    path('base/', base_view),
    path('my_tasks/', my_tasks_view),
    path('new_task/', new_task_view),
    path('add_task/', add_task_view),
    path('account/', account_view),
    path('login/', login_view),
    path('registration/', registration_view),
    path('logout/', logout_view)
]