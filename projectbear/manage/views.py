from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import formset_factory
from main.models import *
from main.forms import ProductForm

# Create your views here.
@login_required
@permission_required('main.view_product')
def manage(request):
    product = Product.objects.all()
    type = Type.objects.all()
    searchtype = request.GET.get('sel','')
    searchtxt = request.GET.get('search','')
    if searchtxt:
        product = product.filter(name__icontains=searchtxt)
    if searchtype > '0':
        product = product.filter(type_id=searchtype)
    context = {
        'product' : product,
        'type' : type,
        'searchtxt' : searchtxt
    }
    return render(request, 'manage/manage.html', context=context)

# หน้าเพิ่มสินค้า
@login_required
@permission_required('main.add_product')
def add_product(request):
    page_title = 'Add Product'
    if request.method == 'GET':
        form = ProductForm()
    else:
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'เพิ่มสินค้าสำเร็จแล้ว')
            return redirect('index')
        else:
            messages.error(request,'Try Again')
    context = {
        'form':form,
        'page_title':page_title
    }
    return render(request,'manage/addproduct_form.html',context=context)

# ลบสินค้า
@login_required
@permission_required('main.delete_product')
def delete_product(request,product_id):
    products = Product.objects.get(id=product_id)
    products.delete()
    return redirect(to='manage')

@login_required
@permission_required('main.change_product')
def product_update(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None ,request.FILES or None , instance=product)
    if form.is_valid():
        product = form.save(commit=False)
        product.save()
        messages.success(request,'เพิ่มสินค้าสำเร็จแล้ว')
        return redirect('index')
    context = {
        'form':form,
        'number':product.id
    }
    return render(request,'manage/editproduct_form.html',context=context)

@login_required
def queue(request):
    order = Order.objects.all().order_by('-id').filter(status=False)
    context ={
        'order':order,
    }
    return render(request,'manage/queue.html', context=context)

def detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    # item = Order_items.objects.get(pk=order.id)
    product = Order_Products.objects.filter(order=order_id)
    # number=[]
    # order_product = Order_Products.objects.all()
    # for i in order_product:
    #     # number.append(Order_Products.objects.all().count(i.product_id))
    #     number.append(Order_Products.objects.all().count(i.product_id))
    #     Order_Products.objects.filter(product_id=i.product_id).delete()
    # print(number)
    context={
        'order':order,
        'product':product,
    }
    return render(request,'manage/detail.html', context=context)