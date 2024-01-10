from rest_framework.views import exception_handler
from django.http import Http404, JsonResponse
from rest_framework.exceptions import *
from rest_framework.status import *



def root_exception_handler(exc, context):
    exception_dict = {
       'Http404' : custom_404_handler,
       'NotFound' : custom_404_handler,
       'AuthenticationFailed' : custom_auth_fail_handler,
       'NotAuthenticated': custom_auth_fail_handler,
       'ParseError' : custom_parse_error_handler,
       'PermissionDenied' : custom_permission_denied_handler,
       'MethodNotAllowed' : custom_method_error_handler,
       'UnsupportedMediaType' : custom_media_error_handler,
       'Throttled' : custom_throttle_error_handler,
       'ValidationError' : custom_validation_error_handler,
       'NotAcceptable' : cutsom_not_accetable_handler,
    }

    exc_name = exc.__class__.__name__
    if exc_name in exception_dict:
        return exception_dict[exc_name](exc= exc)
    
    else:
        response_dict = {}
        response_dict['message'] = exc.__class__.__name__
        response_dict['result'] = exc.__str__()
        response_status = HTTP_500_INTERNAL_SERVER_ERROR
        return JsonResponse(response_dict, safe= False, status = response_status)
    


def custom_404_handler(exc):
    response_dict = {}
    response_status = HTTP_404_NOT_FOUND
    response_dict['message'] = 'ERROR 404'

    if exc.__str__() not in [None, '']:
        response_dict['result'] = exc.__str__()
    else:
        response_dict['result'] = 'Not Found.'

    return JsonResponse(response_dict, safe= False, status = response_status)
        

def custom_auth_fail_handler(exc):
    response_dict = {}
    response_status = HTTP_401_UNAUTHORIZED
    response_dict['message'] = 'ERROR 401'

    if exc.__str__() not in [None, '']:
        response_dict['result'] = exc.__str__()
    else:
        response_dict['result'] = 'Authorization failed.'

    return JsonResponse(response_dict, safe= False, status = response_status)


def custom_parse_error_handler(exc):
    response_dict = {}
    response_status = HTTP_400_BAD_REQUEST
    response_dict['message'] = 'ERROR 400'

    if exc.__str__() not in [None, '']:
        response_dict['result'] = exc.__str__()
    else:
        response_dict['result'] = 'Invalid Data.'

    return JsonResponse(response_dict, safe= False, status = response_status)


def custom_permission_denied_handler(exc):
    response_dict = {}
    response_status = HTTP_403_FORBIDDEN
    response_dict['message'] = 'ERROR 403'

    if exc.__str__() not in [None, '']:
        response_dict['result'] = exc.__str__()
    else:
        response_dict['result'] = 'Permission Denied.'

    return JsonResponse(response_dict, safe= False, status = response_status)


def custom_method_error_handler(exc):
    response_dict = {}
    response_status = HTTP_405_METHOD_NOT_ALLOWED
    response_dict['message'] = 'ERROR 405'

    if exc.__str__() not in [None, '']:
        response_dict['result'] = exc.__str__()
    else:
        response_dict['result'] = 'HTTP request method not allowed.'

    return JsonResponse(response_dict, safe= False, status = response_status)


def custom_media_error_handler(exc):
    response_dict = {}
    response_status = HTTP_415_UNSUPPORTED_MEDIA_TYPE
    response_dict['message'] = 'ERROR 415'

    if exc.__str__() not in [None, '']:
        response_dict['result'] = exc.__str__()
    else:
        response_dict['result'] = 'Media Type Not Supported.'

    return JsonResponse(response_dict, safe= False, status = response_status)


def custom_throttle_error_handler(exc):
    response_dict = {}
    response_status = HTTP_429_TOO_MANY_REQUESTS
    response_dict['message'] = 'ERROR 429'

    if exc.__str__() not in [None, '']:
        response_dict['result'] = exc.__str__()
    else:
        response_dict['result'] = 'Slow down.'

    return JsonResponse(response_dict, safe= False, status = response_status)


def custom_validation_error_handler(exc):
    response_dict = {}
    response_status = HTTP_400_BAD_REQUEST
    response_dict['message'] = 'ERROR 400'

    if exc.__str__() not in [None, '']:
        response_dict['result'] = exc.__str__()
    else:
        response_dict['result'] = 'Invalid Data.'

    return JsonResponse(response_dict, safe= False, status = response_status)


def cutsom_not_accetable_handler(exc):
    response_dict = {}
    response_status = HTTP_406_NOT_ACCEPTABLE
    response_dict['message'] = 'ERROR 406'

    if exc.__str__() not in [None, '']:
        response_dict['result'] = exc.__str__()
    else:
        response_dict['result'] = 'Not Acceptable.'

    return JsonResponse(response_dict, safe= False, status = response_status)