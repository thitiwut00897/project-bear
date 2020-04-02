from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def index(request):
    return HttpResponse('Index มาแล้ว')
def my_login(request):
    return render(request,'login_page.html')
def my_register(request):
    return render(request,'register_page.html')