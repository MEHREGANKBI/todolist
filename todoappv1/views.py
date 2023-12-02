from django.shortcuts import render
from todoappv1.models import Todolist
import json
# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, you're at the root page of the application!")


def retrieve_all(request):
    todolist_list = list(Todolist.objects.all().values())
    todolist_pretty = json.dumps(todolist_list, indent= 2)
    return HttpResponse(todolist_pretty)

def retrieve_undone(request):
    todolist_list = list(Todolist.objects.filter(done_status = False).values())
    todolist_pretty = json.dumps(todolist_list, indent = 2)
    return HttpResponse(todolist_pretty)

def add_activity(request, activity_param):
    activity_param = str(activity_param)
    todolist_object = Todolist()
    todolist_object.done_status = False
    todolist_object.activity_description = activity_param
    todolist_object.save()
    add_response = [ { "request_status" : "success"},
            { "activity_added" : activity_param} ]

    response_pretty = json.dumps(add_response, indent = 2)
    return HttpResponse(response_pretty)

def done(request, id_param):
    id_param = int(id_param)
    todolist_object = Todolist.objects.get(id=id_param)
    todolist_object.done_status = True
    todolist_object.save()
    done_response = [ { "request_status" : "success"},
            { "activity_with_the_following_id_was_set_as_done" : id_param } ]
    response_pretty = json.dumps(done_response , indent = 2)
    return HttpResponse(response_pretty)

