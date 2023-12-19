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
        user_obj = get_object_or_404(User, username= username)
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

def token_authenticate(request_headers):
    jwt_token = request_headers.get('jwt-token', None)
    try:   
        verified_token = jwt.decode(jwt= jwt_token, key= jwt_secret, algorithms= ['HS256',])
    except:
        return False, None
    else:
        return True, verified_token['sub']
        

def user_owns_task(username, task_id):
    user_obj = User.objects.get(username= username)
    task_obj = Task.objects.get(id = task_id)
    if user_obj.id == task_obj.User_id_id :
        return True
    else:
        return False




