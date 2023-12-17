from rest_framework import status


from .serializers import *

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
