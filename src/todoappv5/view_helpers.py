from rest_framework import status
from base64 import b64decode
from django.shortcuts import get_object_or_404
from hashlib import sha512
import jwt
from datetime import datetime


from .serializers import *
from .models import *
from .secrets import salt, jwt_secret


def user_exists(username):
    try:
        user_obj = get_object_or_404(get_user_model(), username= username)
    except:
        return False
    else:
        return True
    

def tag_exists(tag):
    try:
        tag_obj = get_object_or_404(Tag, tag = tag)
    except:
        return False
    else:
        return True
    

def task_exists(task_id):
    try:
        task_obj = get_object_or_404(Task, id = task_id)
    except:
        return False
    else:
        return True


        

def user_owns_task(user_obj, task_id):
    task_obj = Task.objects.get(id = task_id)
    if user_obj == task_obj.User :
        return True
    else:
        return False



