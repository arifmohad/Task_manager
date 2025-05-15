from rest_framework import serializers
from .models import Task
from users.models import CustomUser

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'due_date', 'status', 
                 'completion_report', 'worked_hours', 'created_at', 'updated_at']
        read_only_fields = ['assigned_to', 'created_at', 'updated_at']
    
    def validate(self, data):
        if data.get('status') == 'COMPLETED':
            if not data.get('completion_report'):
                raise serializers.ValidationError("Completion report is required when marking task as completed.")
            if not data.get('worked_hours'):
                raise serializers.ValidationError("Worked hours is required when marking task as completed.")
        return data