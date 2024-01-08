from rest_framework.views import exception_handler
from django.http import Http404
from rest_framework.exceptions import *

from todoappv5.responses import response_dict

def root_exception_handler(exc, context):
    exception_dict = {
       'Http404' : custom_404_handler,
       'NotFound' : custom_404_handler,
       'AuthenticationFailed' : custom_auth_fail_handler,
       'NotAuthenticated': custom_no_auth_handler,
       'ParseError' : custom_parse_error_handler,
       'PermissionDenied' : custom_permission_denied_handler,
       'MethodNotAllowed' : custom_method_error_handler,
       'UnsupportedMediaType' : custom_media_error_handler,
       'Throttled' : custom_throttle_error_handler,
       'ValidationError' : custom_validation_error_handler,
    }

def custom_404_handler(exc):
    pass

def custom_auth_fail_handler(exc):
    pass
def custom_no_auth_handler(exc):
    pass
def custom_parse_error_handler(exc):
    pass
def custom_permission_denied_handler(exc):
    pass
def custom_method_error_handler(exc):
    pass
def custom_media_error_handler(exc):
    pass
def custom_throttle_error_handler(exc):
    pass
def custom_validation_error_handler(exc):
    pass