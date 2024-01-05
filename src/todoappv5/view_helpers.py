from rest_framework import status
from base64 import b64decode
from django.shortcuts import get_object_or_404
from hashlib import sha512
import jwt
from datetime import datetime


from .serializers import *
from .models import *
from .secrets import salt, jwt_secret


def user_exists(username: str) -> bool:
    '''
    Parameters:
        username: A sanitized/deserialized string representing the username field of the user model

    Returns:
        Boolean: True/False

    Description:
        Given a valid username string, check if it exists in the usermodel table, return True if it does, False otherwise.
        This function is case-sensitive and is expected to be called with safe data.
        Invalid values for the <username> argument will cause unexpected errors. 
    '''

    try:
        user_obj = get_object_or_404(get_user_model(), username= username)
    except:
        return False
    else:
        return True
    

def tag_exists(tag: str) -> bool:
    '''
    Parameters: 
        tag: A sanitized str conforming to the rules of the <tag> field of the Tag model.

    Returns:
        Boolean: True/False

    Description:
        Given a deserialized/sanitized tag, return True if the tag already exists in the Tag table (case-sensitive)
        and return False otherwise. Feeding unsanitized strings or non-str tags may result in unexpected return values.
    '''
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




