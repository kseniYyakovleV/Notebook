from django.urls import path
from .views import *

urlpatterns = [
    path('base/', base_view),
    path('my_tasks/', my_tasks_view),
    path('new_task/', new_task_view),
    path('account/', account_view),
    path('login/', login_view),
    path('registration/', registration_view),
    path('logout/', logout_view),
    path('task/<int:task_id>/change/', change_view),
    path('task/<int:task_id>/delete/', delete_view),
    path('task/<int:task_id>/complete/', complete_view),
    path('task/<int:task_id>/not_complete/', not_complete_view),
    path('task/<int:task_id>/', task_view),
    path('test/', test_view),
    path('change_password/', change_password_view),
    path('delete_account/', delete_account_view),
    path('change_username/', change_username_view)
]