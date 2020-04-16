from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# def createorder(request):
#     return HttpResponse('Order Page.')
def history_payment(request):
    return HttpResponse('history_payment')
def all_report(request):
    return HttpResponse('All report.')