from rest_framework.status import HTTP_200_OK



def make_success_response(result, message : str = 'SUCCESS...') -> tuple[dict,int] :
    '''
    Parameters: 
        result: The payload of the message. 
        message: The message of the response. Currently sends a default text and doesn't provide any extra information.

    Returns:
        response_table: a tuple of [dict, int]. The int represents the HTTP request status. The dict is the response body.

    Decription:
        Given a payload and a message corresponding to a successful HTTP request, return a tuple of
        the response body and the HTTP request status.
    '''
    response_status = HTTP_200_OK
    response_dict = {}

    response_dict['message'] = message
    response_dict['result'] = result

    response_tuple = response_dict, response_status
    return response_tuple