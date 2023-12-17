from rest_framework import status
from base64 import b64decode
from django.shortcuts import get_object_or_404
from hashlib import sha512

from .serializers import *
from .models import User
from .secrets import salt

def validate_b64_userpass(b64_userpass):
    try:
        validated_userpass = b64decode(bytes(b64_userpass, encoding = 'utf-8'), validate= True).decode(encoding='utf-8') 
        delimiter_idx = validated_userpass.index(':')
    except:
        return False, ('ERROR...', 'Invalid auth header.')
    else:
        username = validated_userpass[:delimiter_idx]
        password = validated_userpass[delimiter_idx + 1 :]
        return True, (username, password)



def authenticate_userpass(username,password):
    try:
        user_obj = get_object_or_404(User,username = username)
    except:
        return False, ('ERROR...', 'Invalid username or password.')
    else:
        salted_password = salt + password
        password_hash = sha512(bytes(salted_password, encoding = 'utf-8')).hexdigest()
        if user_obj.password == password_hash: 
            return True, ('SUCCESS...' , 'This is a jwt token')
        else:
            return False, ('ERROR...', 'Invalid username or password.')




def get_todolist_data(retrieval_mode):
    pass
#     response_result = None
#     response_message = None
#     response_status = None

#     if retrieval_mode == 'ALL':
#         retrieval_objects = Todolist.objects.all()
#         serialized_objects = TodolistSerializer(retrieval_objects, many = True).data
#         response_result = serialized_objects
#         response_message = 'The retrieval request was completed without errors.'
#         response_status = status.HTTP_200_OK

#     elif retrieval_mode == 'DONE':
#         retrieval_objects = Todolist.objects.filter(done_status = True)
#         serialized_objects = GETTodolistSerializer(retrieval_objects, many = True).data
#         response_result = serialized_objects 
#         response_message = 'The retrieval request was completed without errors.' 
#         response_status = status.HTTP_200_OK

#     elif retrieval_mode == 'UNDONE':
#         retrieval_objects = Todolist.objects.filter(done_status = False)
#         serialized_objects = GETTodolistSerializer(retrieval_objects, many = True).data
#         response_result = serialized_objects
#         response_message = 'The retrieval request was completed without errors.'
#         response_status = status.HTTP_200_OK

#     else:
#         response_result = 'ERROR!'
#         response_message = 'Value Error encountered. Valid values: ALL, DONE, UNDONE!'
#         response_status = status.HTTP_400_BAD_REQUEST


#     return response_result, response_message, response_status
