from django.shortcuts import render
from django.http import HttpResponse
from main.models import Order,Order_Products,Payment
# Create your views here.
def each_a_order(request):
    pass
def history_payment(request):
    return HttpResponse('history_payment')
def all_report(request):
    order = Order.objects.all().filter(status=True)
    context={
        'order':order
    }
    return render(request,'report/all_report.html',context=context)