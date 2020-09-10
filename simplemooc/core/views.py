from django.shortcuts import render
from django.http import HttpResponse  # necessario em todas views

from django.contrib import messages


# Create your views here.


def home(request):
    return render(request, 'home.html', {})


def contact(request):
    return render(request, 'contact.html', {})
