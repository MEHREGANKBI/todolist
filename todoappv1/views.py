from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, you're at the root page of the application!")
