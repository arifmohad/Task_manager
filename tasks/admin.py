from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'due_date')
    list_filter = ('status', 'assigned_to')
    search_fields = ('title', 'description')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superadmin:
            return qs
        return qs.filter(assigned_to__admin=request.user)

admin.site.register(Task, TaskAdmin)