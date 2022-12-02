from django.http import HttpResponse
from django.shortcuts import render, redirect


def home(request):
  hello = "Hello, World!"
  context = {
    'hello': hello,
  }
  return render(request, 'main/home.html', context)