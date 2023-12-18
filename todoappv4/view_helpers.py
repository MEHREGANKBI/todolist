from rest_framework import status
from base64 import b64decode
from django.shortcuts import get_object_or_404
from hashlib import sha512
import jwt
from datetime import datetime


from .serializers import *
from .models import User
from .secrets import salt, jwt_secret


def user_exists(username):
    try:
        user_obj = get_object_or_404(User, username= username)
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
