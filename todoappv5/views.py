from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import get_user_model


from .serializers import *
from .responses import response_dict
from .view_helpers import *


class TaskView(APIView):
    pass

    # def get_user_tasks(self,username, type_param):
    #     response_status = None
    #     response_message = None
    #     response_result = None

    #     user_id = User.objects.get(username = username).id # type: ignore
    #     user_queryset = Task.objects.filter(User_id = user_id).select_related('Tag_id', 'User_id')

    #     if type_param == 'ALL':
    #         pass
    #     elif type_param == 'DONE':
    #         user_queryset = user_queryset.filter(is_complete = True)
    #     elif type_param == 'UNDONE':
    #         user_queryset = user_queryset.filter(is_complete = False)
    #     else:
    #         response_status = status.HTTP_400_BAD_REQUEST
    #         response_message = 'ERROR...'
    #         response_result = 'Invalid filter.'
    #         return response_message, response_result, response_status

    #     if user_queryset.exists():
    #         serilized_user_data = TaskGETSerializer(user_queryset, many = True)
    #         response_result = serilized_user_data.data
    #         response_status = status.HTTP_200_OK
    #         response_message = 'SUCCESS...'
    #     else:
    #         response_status = status.HTTP_404_NOT_FOUND
    #         response_message = 'ERROR...'
    #         response_result = 'You currently don\'t have any tasks.'

    #     return response_message, response_result, response_status


    # def get(self, request, type_param):
    #     type_param = type_param.strip().upper()
    #     response_status = None

    #     token_is_valid, username = token_authenticate(request.headers)
    #     if token_is_valid and user_exists(username):
    #         response_dict['message'], response_dict['result'], response_status = self.get_user_tasks(username,type_param) # type: ignore


    #     # elif token_is_valid:
    #     #     response_status = status.HTTP_404_NOT_FOUND
    #     #     response_dict['message'] = 'ERROR...'
    #     #     response_dict['result'] = 'User not found.'

    #     else:
    #         response_status = status.HTTP_401_UNAUTHORIZED
    #         response_dict['message'] = 'ERROR...'
    #         response_dict['result'] = 'You need to sign in.'
        
    #     return JsonResponse(response_dict, safe= False, status= response_status)


    

    # def post(self, request):
    #     response_status = None

    #     token_is_valid, username = token_authenticate(request.headers)
    #     if token_is_valid and user_exists(username):
    #         pass
    #     else:
    #         response_status = status.HTTP_401_UNAUTHORIZED
    #         response_dict['message'] = 'ERROR...'
    #         response_dict['result'] = 'You need to sign in.'
    #         return JsonResponse(response_dict, safe= False, status = response_status)
    #     # If the following json is not valid, it'll send an automatic response, the pattern 
    #     # of which is out of my control and is different from my unified response pattern.
    #     # Possible solutions: 
    #     # 1: validate the json before handing it to the serializer which defeats the purpose of using serializers.
    #     # 2: use try except on the parsing line which apparently degrades performance.
    #     deserialized_data = POSTSerializer(data= request.data)

    #     if deserialized_data.is_valid():
    #         save_status = deserialized_data.save(username= username)
    #         response_dict['message'] =  'SUCCESS!'
    #         response_dict['result'] = save_status # type: ignore
    #         response_status = status.HTTP_200_OK

    #     else:
    #         response_dict['message'] = "ERROR!"
    #         response_dict['result'] = deserialized_data.errors # type: ignore
    #         response_status = status.HTTP_400_BAD_REQUEST

    #     return JsonResponse(response_dict, safe= False, status =response_status)
    

    # def delete(self, request, id_param):
    #     response_status = None

    #     token_is_valid, username = token_authenticate(request.headers)
    #     if token_is_valid and user_exists(username) and task_exists(id_param):
    #         # now we check if the task with the given id is owned by the user whose username is in the token.
    #         if user_owns_task(username, id_param):
    #             task_obj = Task.objects.get(id = id_param)
    #             task_obj.delete()
    #             response_status = status.HTTP_200_OK
    #             response_dict['message'] = 'SUCCESS...'
    #             response_dict['result'] = 'The task was successfully removed.'
    #         else:
    #             response_status = status.HTTP_403_FORBIDDEN
    #             response_dict['message'] = 'ERROR...'
    #             response_dict['result'] = 'You do not have the permission to complete this action.'
        
    #     elif token_is_valid and user_exists(username):
    #         response_status = status.HTTP_404_NOT_FOUND
    #         response_dict['message'] = 'ERROR...'
    #         response_dict['result'] = 'Task not found.'

    #     else:
    #         response_status = status.HTTP_401_UNAUTHORIZED
    #         response_dict['message'] = 'ERROR...'
    #         response_dict['result']  = 'You need to sign in.'       
        


    #     return JsonResponse(response_dict, safe= False, status = response_status)
        

    # def put(self, request):
    #     response_status = None

    #     token_is_valid, username = token_authenticate(request.headers)
    #     if token_is_valid and user_exists(username):
    #         deserialized_data = PUTTaskSerializer(data= request.data)
    #         #this serializer will check if the task exists too so we don't have to check seperately.
    #         if deserialized_data.is_valid() and user_owns_task(username, deserialized_data.validated_data['id']): # type: ignore
    #             # At this point we know the user is legit and owns the task. the task exists too. so green light for edit.
    #             save_status = deserialized_data.save()
    #             response_status = status.HTTP_200_OK
    #             response_dict['message'] = 'SUCCESS...'
    #             response_dict['result'] = save_status  # type: ignore

    #         elif deserialized_data.is_valid():
    #             response_status = status.HTTP_403_FORBIDDEN
    #             response_dict['message'] = 'ERROR...'
    #             response_dict['result'] = 'You do not have the permission to complete this action.'

    #         else:
    #             response_status = status.HTTP_404_NOT_FOUND
    #             response_dict['message'] = 'ERROR...'
    #             response_dict['result'] = 'Task not found due to invalid data.' 
                


    #     else:
    #         response_status = status.HTTP_401_UNAUTHORIZED
    #         response_dict['message'] = 'ERROR...'
    #         response_dict['result'] = 'You need to sign in.'


    #     return JsonResponse(response_dict, safe= False, status= response_status)



class CustomAuth(APIView):


    def signup(self, request):
        deserialized_data = UserCreationSerializer(data= request.data)

        if deserialized_data.is_valid():
            deserialized_data.save()

            response_status = status.HTTP_200_OK
            response_message = 'SUCCESS...'
            response_result = 'Your account was created. You can sign in now.'

        else:
            response_status = status.HTTP_400_BAD_REQUEST
            response_message = 'ERROR...'
            response_result = deserialized_data.errors

        return response_message, response_result, response_status




    def post(self,request):
        response_status = None
        
        response_dict['message'], response_dict['result'], response_status = self.signup(request) # type: ignore 

        return JsonResponse(response_dict, safe= False, status = response_status)
