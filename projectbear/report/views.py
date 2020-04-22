from django.shortcuts import render
from django.http import HttpResponse
from main.models import Order,Order_Products,Payment
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum,Avg,Min,Max
# Create your views here.
@login_required
def history_payment(request): #ดูประวัติการสั่งซื้อในแต่ละบัญชีผู้ใช้
    history = Order.objects.filter(customer=request.user.id)
    context={
        'history':history
    }
    return render(request,'report/history_each_a_user.html',context=context)

@login_required
@permission_required('main.view_order')
def all_report(request): #สรุปยอดขาย
    order = Order.objects.all().filter(status=True)
    order_pro = Order_Products.objects.all()
    context={
        'order':order,
        'order_sum': order.aggregate(Sum('total_price'))['total_price__sum'],
        'order_avg':order.aggregate(Avg('total_price'))['total_price__avg'],
        'order_max':order.aggregate(Max('total_price'))['total_price__max'],
        'order_min':order.aggregate(Min('total_price'))['total_price__min'],
        'order_sumamount':order_pro.aggregate(Sum('amount'))['amount__sum']
    }
    return render(request,'report/all_report.html',context=context)