from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def test(request):
    return HttpResponse("hi")



def home_view(request):
    return render(request, 'home/home.html')