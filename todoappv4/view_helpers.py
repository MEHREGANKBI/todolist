from rest_framework import status
from base64 import b64decode
from django.shortcuts import get_object_or_404
from hashlib import sha512
import jwt
from datetime import datetime


from .serializers import *
from .models import User
from .secrets import salt, jwt_secret

def create_jwt_token(username):
    # 24hrs
    expiry_unix_epoch = int(datetime.utcnow().timestamp()) + 86400
    jwt_payload = { 'sub' : username,
                    'exp' : expiry_unix_epoch }
    
    jwt_token = jwt.encode(payload= jwt_payload, key= jwt_secret, algorithm= 'HS256')
    return jwt_token

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
            jwt_token = create_jwt_token(username)
            return True, ('SUCCESS...' , jwt_token)
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
