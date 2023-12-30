from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import *

def task_exists_validator(task_id):
    try:
        task_obj = get_object_or_404(Task, id = task_id)
    except:
        raise serializers.ValidationError('Task not found')