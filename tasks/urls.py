from django.urls import path
from .views import TaskListCreateView, TaskUpdateView, TaskReportView
from django.urls import path
from . import views
urlpatterns = [
    path('add_task/', views.admin_tasks, name='add_task'),
    path('update-task-status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('submit-task-report/<int:task_id>/', views.submit_task_report, name='submit_task_report'),
    path('delete_task/<int:task_id>/',views.delete_task, name='delete_task'),
    path('delete_task_admin/<int:task_id>/',views.delete_task_admin, name='delete_task_admin'),


]