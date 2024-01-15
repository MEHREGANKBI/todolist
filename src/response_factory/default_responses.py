from rest_framework.status import HTTP_200_OK
def make_success_response(result, message = 'SUCCESS...') -> tuple[dict,int] :
    response_status = HTTP_200_OK
    response_dict = {}

    response_dict['message'] = message
    response_dict['result'] = result

    return response_dict, response_status