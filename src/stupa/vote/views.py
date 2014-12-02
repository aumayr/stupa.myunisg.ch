from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context_dict = { 'message': "I am text from the context" }
    return render(request, 'index.html', context_dict)
