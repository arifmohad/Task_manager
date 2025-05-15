from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from users.models import CustomUser

class TaskListCreateView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class TaskReportView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin() or user.is_admin():
            return Task.objects.filter(status='COMPLETED')
        return Task.objects.none()
from django.contrib.auth import get_user_model

User = get_user_model()    
from .models import Task
def admin_tasks(request):
    # Assuming user is admin and can see all tasks assigned to their users
    users = User.objects.filter(role='USER')  # Adjust this if you assign users differently
    tasks = Task.objects.all()  # Or filter tasks assigned to users under this admin

    if request.method == "POST":
        # handle task creation here (you can create a form class for this)
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')

        assigned_user = get_object_or_404(User, id=assigned_to_id)

        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_user,
            due_date=due_date,
            status=status
        )
        return redirect('admin_page')

    return render(request, 'admin_tasks.html', {'tasks': tasks, 'users': users})


def update_task_status(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
        new_status = request.POST.get('status')

        if new_status in ['Pending', 'In Progress', 'Completed']:
            task.status = new_status
            task.save()

    return redirect('user_dashboard')

def submit_task_report(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
        worked_hours = request.POST.get('worked_hours')

        try:
            task.worked_hours = float(worked_hours)
            task.save()
        except ValueError:
            pass  # You can add a message to notify the user of invalid input

    return redirect('user_dashboard')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Optional: check if the user is allowed to delete this task
    if request.user == task.assigned_to or request.user.is_superuser:
        task.delete()
    else:
        messages.error(request, "You are not authorized to delete this task.")

    return redirect('sadmin')

from django.contrib import messages

def delete_task_admin(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, "Task deleted successfully.")
    return redirect('admin_page')