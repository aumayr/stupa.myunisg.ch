from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Django says hey there world!")
