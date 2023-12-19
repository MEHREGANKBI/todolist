from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from base64 import b64decode

from .serializers import *
from .responses import response_dict
from .view_helpers import *


class TaskView(APIView):

    def get_user_tasks(self,username, type_param):
        response_status = None
        response_message = None
        response_result = None

        user_id = User.objects.get(username = username).id # type: ignore
        user_queryset = Task.objects.filter(User_id = user_id).select_related('Tag_id', 'User_id')

        if type_param == 'ALL':
            pass
        elif type_param == 'DONE':
            user_queryset = user_queryset.filter(is_complete = True)
        elif type_param == 'UNDONE':
            user_queryset = user_queryset.filter(is_complete = False)
        else:
            response_status = status.HTTP_400_BAD_REQUEST
            response_message = 'ERROR...'
            response_result = 'Invalid filter.'
            return response_message, response_result, response_status

        if user_queryset.exists():
            serilized_user_data = TaskGETSerializer(user_queryset, many = True)
            response_result = serilized_user_data.data
            response_status = status.HTTP_200_OK
            response_message = 'SUCCESS...'
        else:
            response_status = status.HTTP_404_NOT_FOUND
            response_message = 'ERROR...'
            response_result = 'You currently don\'t have any tasks.'

        return response_message, response_result, response_status


    def get(self, request, type_param):
        type_param = type_param.strip().upper()
        response_status = None

        token_is_valid, username = token_authenticate(request.headers)
        if token_is_valid and user_exists(username):
            response_dict['message'], response_dict['result'], response_status = self.get_user_tasks(username,type_param) # type: ignore


        # elif token_is_valid:
        #     response_status = status.HTTP_404_NOT_FOUND
        #     response_dict['message'] = 'ERROR...'
        #     response_dict['result'] = 'User not found.'

        else:
            response_status = status.HTTP_401_UNAUTHORIZED
            response_dict['message'] = 'ERROR...'
            response_dict['result'] = 'You need to sign in.'
        
        return JsonResponse(response_dict, safe= False, status= response_status)


    

    def post(self, request):
        response_status = None

        token_is_valid, username = token_authenticate(request.headers)
        if token_is_valid and user_exists(username):
            pass
        else:
            response_status = status.HTTP_401_UNAUTHORIZED
            response_dict['message'] = 'ERROR...'
            response_dict['result'] = 'You need to sign in.'
            return JsonResponse(response_dict, safe= False, status = response_status)
        # If the following json is not valid, it'll send an automatic response, the pattern 
        # of which is out of my control and is different from my unified response pattern.
        # Possible solutions: 
        # 1: validate the json before handing it to the serializer which defeats the purpose of using serializers.
        # 2: use try except on the parsing line which apparently degrades performance.
        deserialized_data = POSTSerializer(data= request.data)

        if deserialized_data.is_valid():
            save_status = deserialized_data.save(username= username)
            response_dict['message'] =  'SUCCESS!'
            response_dict['result'] = save_status # type: ignore
            response_status = status.HTTP_200_OK

        else:
            response_dict['message'] = "ERROR!"
            response_dict['result'] = deserialized_data.errors # type: ignore
            response_status = status.HTTP_400_BAD_REQUEST

        return JsonResponse(response_dict, safe= False, status =response_status)
    

    def delete(self, request, id_param):
        response_status = None

        token_is_valid, username = token_authenticate(request.headers)
        if token_is_valid and user_exists(username) and task_exists(id_param):
            # now we check if the task with the given id is owned by the user whose username is in the token.
            if user_owns_task(username, id_param):
                task_obj = Task.objects.get(id = id_param)
                task_obj.delete()
                response_status = status.HTTP_200_OK
                response_dict['message'] = 'SUCCESS...'
                response_dict['result'] = 'The task was successfully removed.'
            else:
                response_status = status.HTTP_403_FORBIDDEN
                response_dict['message'] = 'ERROR...'
                response_dict['result'] = 'You do not have the permission to complete this action.'
        
        elif token_is_valid and user_exists(username):
            response_status = status.HTTP_404_NOT_FOUND
            response_dict['message'] = 'ERROR...'
            response_dict['result'] = 'Task not found.'

        else:
            response_status = status.HTTP_401_UNAUTHORIZED
            response_dict['message'] = 'ERROR...'
            response_dict['result']  = 'You need to sign in.'       
        


        return JsonResponse(response_dict, safe= False, status = response_status)
        

    def put(self, request):
        response_status = None

        token_is_valid, username = token_authenticate(request.headers)
        if token_is_valid and user_exists(username):
            deserialized_data = PUTTaskSerializer(data= request.data)
            #this serializer will check if the task exists too so we don't have to check seperately.
            if deserialized_data.is_valid() and user_owns_task(username, deserialized_data.validated_data['id']): # type: ignore
                # At this point we know the user is legit and owns the task. the task exists too. so green light for edit.
                save_status = deserialized_data.save()
                response_status = status.HTTP_200_OK
                response_dict['message'] = 'SUCCESS...'
                response_dict['result'] = save_status  # type: ignore

            elif deserialized_data.is_valid():
                response_status = status.HTTP_403_FORBIDDEN
                response_dict['message'] = 'ERROR...'
                response_dict['result'] = 'You do not have the permission to complete this action.'

            else:
                response_status = status.HTTP_404_NOT_FOUND
                response_dict['message'] = 'ERROR...'
                response_dict['result'] = 'Task not found due to invalid data.' 
                


        else:
            response_status = status.HTTP_401_UNAUTHORIZED
            response_dict['message'] = 'ERROR...'
            response_dict['result'] = 'You need to sign in.'


        return JsonResponse(response_dict, safe= False, status= response_status)



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
