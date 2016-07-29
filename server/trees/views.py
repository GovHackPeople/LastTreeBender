from django.shortcuts import render
from django.http import HttpResponse
import os

def index(request):
    return HttpResponse("Trees!")

def importData(request):
    os.mkdir()
    return HttpResponse("Import done")