from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from base64 import b64decode

from .serializers import *
from .responses import response_dict
from .view_helpers import *


class TaskView(APIView):

    def get(self, request, type_param):
        type_param = type_param.strip().upper()
        response_status = None

        token_is_valid, username = token_authenticate(request.headers)
        if token_is_valid and user_exists(username):
            response_dict['message'], response_dict['result'], response_status = get_user_tasks(username,type_param)


        elif token_is_valid:
            response_status = status.HTTP_404_NOT_FOUND
            response_dict['message'] = 'ERROR...'
            response_dict['result'] = 'User not found.'

        else:
            response_status = status.HTTP_401_UNAUTHORIZED
            response_dict['message'] = 'ERROR...'
            response_dict['result'] = 'You need to sign in.'
        
        return JsonResponse(response_dict, safe= False, status= response_status)


    

#     def post(self, request):
#         response_status = None

#         # If the following json is not valid, it'll send an automatic response, the pattern 
#         # of which is out of my control and is different from my unified response pattern.
#         # Possible solutions: 
#         # 1: validate the json before handing it to the serializer which defeats the purpose of using serializers.
#         # 2: use try except on the parsing line which apparently degrades performance.
#         serialized_data = TodolistSerializer(data= request.data)

#         if serialized_data.is_valid():
#             serialized_data.save()
#             response_dict['result'] =  'SUCCESS!'
#             response_dict['message'] = 'Your composition request was completed without errors!'
#             response_status = status.HTTP_200_OK

#         else:
#             response_dict['result'] = "ERROR!"
#             response_dict['message'] = serialized_data.errors # type: ignore
#             response_status = status.HTTP_400_BAD_REQUEST

#         return JsonResponse(response_dict, safe= False, status =response_status)
    

#     def delete(self, request, id_param):
#         response_status = None

#         deserialized_data = DELETETodolistSerializer(data = {'id' : id_param}) # type: ignore

#         if deserialized_data.is_valid():
#             del_obj = Todolist.objects.get(id = deserialized_data.validated_data['id']) # type: ignore
#             del_obj.delete()
#             response_dict['result'] = 'SUCCESS!'
#             response_dict['message'] = 'The deletion was completed without errors!' 
#             response_status = status.HTTP_200_OK

#         else:
#             response_dict['result'] = 'ERROR!'
#             response_dict['message'] = 'Object with the given id was not found!'
#             response_status = status.HTTP_404_NOT_FOUND            
        
#         # try:
#         #     deletion_obj = get_object_or_404(Todolist, id = id_param)
#         #     deletion_obj.delete()
#         #     response_dict['result'] = 'SUCCESS!'
#         #     response_dict['message'] = 'The deletion was completed without errors!' 
#         #     response_status = status.HTTP_200_OK
        
#         # except Http404:
#         #     response_dict['result'] = 'ERROR!'
#         #     response_dict['message'] = 'Object with the given id was not found!'
#         #     response_status = status.HTTP_404_NOT_FOUND


#         return JsonResponse(response_dict, safe= False, status = response_status)
        

#     def put(self, request):
#         response_status = None

#         deserialized_data = PUTTodolistSerializer(data= request.data)

#         if deserialized_data.is_valid():
#             # since both id and done_status are validated, we won't face errors in the 3 following lines.
#             update_obj = Todolist.objects.get(id=deserialized_data.validated_data['id']) # type: ignore
#             update_obj.done_status = deserialized_data.validated_data['done_status'] # type: ignore
#             update_obj.save()
#             response_dict['result'] = 'SUCCESS!'
#             response_dict['message'] = 'Your update request was completed without errors.'
#             response_status = status.HTTP_200_OK

#         else:
#             response_dict['result'] = 'ERROR!'
#             response_dict['message'] = deserialized_data.errors # type: ignore
#             response_status = status.HTTP_400_BAD_REQUEST
        
#         return JsonResponse(response_dict, safe= False, status= response_status)



class CustomAuth(APIView):

    def create_jwt_token(self,username):
        # 24hrs
        expiry_unix_epoch = int(datetime.utcnow().timestamp()) + 86400
        jwt_payload = { 'sub' : username,
                        'exp' : expiry_unix_epoch }
        
        jwt_token = jwt.encode(payload= jwt_payload, key= jwt_secret, algorithm= 'HS256')
        return jwt_token
    
    def create_new_user(self,username,password):
        response_status = None
        response_message = None
        response_result = None

        salted_password = salt + password
        hashed_password = sha512(bytes(salted_password, encoding = 'utf-8')).hexdigest()
        new_user = { 'username' : username,
                     'password' : hashed_password}
        
        deserialized_user = UserSerializer(data= new_user)
        if deserialized_user.is_valid():
            deserialized_user.save()
            jwt_token = self.create_jwt_token(username)
            response_status = status.HTTP_200_OK
            response_message = 'SUCCESS...'
            response_result = jwt_token

        else:
            response_status = status.HTTP_400_BAD_REQUEST
            response_message = 'ERROR...'
            response_result = deserialized_user.errors

        return response_message, response_result, response_status



    def authenticate_userpass(self,username,password):
        try:
            user_obj = get_object_or_404(User,username = username)
        except:
            return False, ('ERROR...', 'Invalid username or password.')
        else:
            salted_password = salt + password
            password_hash = sha512(bytes(salted_password, encoding = 'utf-8')).hexdigest()
            if user_obj.password == password_hash: 
                jwt_token = self.create_jwt_token(username)
                return True, ('SUCCESS...' , jwt_token)
            else:
                return False, ('ERROR...', 'Invalid username or password.')
            

    def validate_b64_userpass(self, b64_userpass):
        # TODO: add more checks to make sure username or password don't contain weird characters.
        try:
            validated_userpass = b64decode(bytes(b64_userpass, encoding = 'utf-8'), validate= True).decode(encoding='utf-8') 
            delimiter_idx = validated_userpass.index(':')
        except:
            return False, ('ERROR...', 'Invalid auth header.')
        else:
            username = validated_userpass[:delimiter_idx]
            password = validated_userpass[delimiter_idx + 1 :]
            return True, (username, password)


    def signin(self,request):
        response_status = None
        response_message = None
        response_result = None
        b64_userpass = request.headers.get('custom-auth', None)

        combo_is_valid, payload = self.validate_b64_userpass(b64_userpass)
        if combo_is_valid :
            username, password = payload
            is_authenticated, auth_payload = self.authenticate_userpass(username,password)
            if is_authenticated:
                response_status = status.HTTP_200_OK
                response_message, response_result = auth_payload
            else:
                response_status = status.HTTP_404_NOT_FOUND
                response_message, response_result = auth_payload
            
        else:
            response_status = status.HTTP_400_BAD_REQUEST
            response_message, response_result = payload   

        return response_message, response_result, response_status         




    def signup(self, request):
        response_status = None
        response_message = None
        response_result = None
        b64_userpass = request.headers.get('custom-auth', None)

        combo_is_valid, payload = self.validate_b64_userpass(b64_userpass)
        if combo_is_valid:
            username, password = payload
            
            response_message, response_result, response_status = self.create_new_user(username, password)


        else:
            response_status = status.HTTP_400_BAD_REQUEST
            response_message, response_result = payload

        return response_message, response_result, response_status




    def post(self,request):
        response_status = None
        path_requested = request.path
        signup_path = '/todoappv4/signup/'
        signin_path = '/todoappv4/signin/'


        if path_requested == signin_path:
            response_dict['message'], response_dict['result'], response_status = self.signin(request)

        elif path_requested == signup_path:
            response_dict['message'], response_dict['result'], response_status = self.signup(request) # type: ignore 

        else:
            response_dict['message'] = 'ERROR...'
            response_dict['result'] = 'Invalid URL.'
            response_status = status.HTTP_404_NOT_FOUND


        return JsonResponse(response_dict, safe= False, status = response_status)
