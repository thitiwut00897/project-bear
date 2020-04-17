from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import formset_factory
from main.models import Type, Product
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
    return render(request,'manage/product_form.html',context=context)
# เพิ่มเข้าในตาราง product
@login_required
def add_to_database(request):
    page_title = 'Add Product'
    type = Type.objects.all()
    create= ''
    notice = ''
    if request.method == 'POST' and request.FILES['picture']:
        number = request.POST.get('txt_1')
        try:
            create = Product(
                    type=Type.objects.get(pk=number),
                    name=request.POST.get('txt_2'),
                    stock=request.POST.get('txt_3'),
                    price=request.POST.get('txt_4'),
                    picture=request.FILES['picture'],
                )
            create.save()
            notice = 'การเพิ่มสินค้าของคุณสำเร็จแล้ว -> หมายเลขสินค้าที่ %s' % (create.id)
        except ValueError:
            notice = 'โอ๊ะ! ประเภทข้อมูลผิดพลาด'
    context = {
        'create':create,
        'notice':notice,
        'type':type,
        'page_title':page_title
    }
    return render(request, 'manage/product_form.html', context=context)

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
    page_title = 'Update Product = %d' %product_id
    product = Product.objects.get(pk=product_id)
    type = Type.objects.all()
    notice = ''
    if request.method == 'POST':
        product.name = request.POST.get('txt_2')
        product.type_id = request.POST.get('txt')
        product.stock = request.POST.get('txt_3')
        try:
            product.price = request.POST.get('txt_4')
            product.save()
            notice = 'บันทึกข้อมูลเรียบร้อยแล้ว'
        except ValueError:
            notice = 'โอ๊ะ! ประเภทข้อมูลผิดพลาด'
    context={
        'num':product_id,
        'product':product,
        'type':type,
        'notice':notice,
        'page_title':page_title
    }
    return render(request,'manage/product_form2.html',context=context)

# @login_required
# def queue(request):
#     return render(request, 'manage/queue.html')

