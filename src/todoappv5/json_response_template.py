# WARNING:
# This dictionary acts as a template for the JSON responses. Thus, I heavily discourage you from 
# importing this dictionary into other files and using them there since in the presence of certain bugs
# it will lead to leaking the user data to unauthorized users.

from typing import Any
response_dict: dict[Any, Any]
response_dict = {
    'message' :  'This is a message to let the client know what happened.',
    'result'  :  'This is the payload, which either contains the response data or errors in detail.'
}