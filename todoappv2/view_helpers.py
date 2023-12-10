# def done_status_checker(received_data):
#     try:
#         temp = received_data['done_status']
#     except KeyError:
#         ret_val = { "usage_error" : 'The key "done_status" must exist!'}
#         return Response(ret_val, status= status.HTTP_400_BAD_REQUEST)
