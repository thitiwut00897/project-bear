from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from main.forms import UpdateProfile,ProfileForm
from main.models import *
# Create your views here.

def index(request):
    product = Product.objects.all()
    type = Type.objects.all()
    search = request.GET.get('search','')
    searchtype = request.GET.get('sel','')
    if search:
        product = product.filter(name__icontains=search)
    if searchtype > '0':
        product = product.filter(type_id=searchtype)
    context = {
        'product':product,
        'type':type,
    }
    return render(request, 'main/index.html', context=context)

def my_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            messages.info(request,'ชื่อผู้ใช้ หรือ รหัสผ่านผิด โปรดลองอีกครั้ง')
    return render(request,'login_page.html',context=context)

def my_logout(request):
    basket = Order_items.objects.all()
    basket.delete()
    logout(request)
    return redirect('index')
    
@permission_required('auth.user.Can_add_user')
def my_register(request):
    if request.method == 'POST':
        username = request.POST.get('u_name','')
        firstname = request.POST.get('f_name','')
        lastname = request.POST.get('l_name','')
        email = request.POST.get('email','')
        password1 = request.POST.get('password1','')
        password2 = request.POST.get('password2','')
        tel = request.POST.get('telephone','')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username นี้มีคนใช้แล้ว')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email นี้เคยลงทะเบียนแล้ว')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username = username,
                    first_name = firstname,
                    last_name = lastname,
                    email = email,
                    password = password1,
                )
                user2 = Profile.objects.create(
                    user_id = user.id,
                    tel = tel
                )
                user.save()
                user2.save()
                messages.success(request,'ลงทะเบียนเรียบร้อยแล้ว กรุณาเข้าสู่ระบบ')
                return redirect('login')
        else:
            messages.info(request,'รหัสผ่านไม่ตรงกัน')
            return redirect('register')
    return render(request,template_name='register_page.html')

# เปลี่ยนรหัสผ่าน
@login_required
def change_password(request):
    page_title = 'Change Password'
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.info(request,'รหัสผ่านถูกเปลี่ยนแล้ว')
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    context={
        'form':form ,
        'page_title':page_title
        }
    return render(request,template_name='changepw_page.html',context=context)

@login_required
@permission_required('main.order_items.Can_view_order_items')
def basket(request):
    basket = Order_items.objects.all()
    total = 0
    for i in basket:
        total += i.item_price
    context={
        'basket':basket,
        'total': total
    }
    return render(request, 'main/basket.html',context=context)

@login_required
@permission_required('main.order_items.Can_add_order_items')
def addtobasket(request,product_id):
    product = Product.objects.get(pk=product_id)
    item = Order_items.objects.all()
    unit = 1
    if item:
        for i in item:
            if i.item_no_id == product_id:
                item = Order_items.objects.get(id=i.id)
                item.unit += 1
                item.item_price = item.unit*product.price
                break
            else:
                item = Order_items()
                item.item_no_id= product.id
                item.price = product.price
                item.unit = unit
                item.item_price = product.price
    else:
        item = Order_items()
        item.item_no_id = product.id
        item.price = product.price
        item.unit = unit
        item.item_price = product.price
    item.save()
    messages.info(request,'เพิ่มสินค้าลงตะกร้าแล้ว')
    return redirect('index')

@login_required
@permission_required('main.order_items.Can_delete_order_items')
def deletetobasket(request,basket_id):
    item = Order_items.objects.get(pk=basket_id)
    item.delete()
    messages.info(request,'ลบสินค้าในตะกร้าแล้ว')
    return redirect('basket')

@login_required
def payment(request):
    total = 0
    item = Order_items.objects.all()
    for i in item:
        total += i.item_price
    orders = Order.objects.create(
        total_price = total,
        cust_name = request.user.username,
        
    )
    orders.save()
    item.delete()
    order = Order.objects.all()
    context ={
        'order':order,
    }
    return render(request,'main/payment.html', context=context)

@login_required
def profile(request):
    return render(request,'profile.html')

@login_required
@permission_required('main.profile.Can_change_profile')
def update_profile(request):
    if request.method == 'POST':
        form1 = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        form2 = UpdateProfile(request.POST,instance=request.user)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.info(request,'บันทึกข้อมูลแล้ว')
            return redirect('index')
    else:
        form1 = ProfileForm(instance=request.user.profile)
        form2 = UpdateProfile(instance=request.user)
    context={
        'form1':form1,
        'form2':form2
    }
    return render(request,'profile.html',context=context)

def acceptorder(request, order_id):
    order= Order.objects.get(pk=order_id)
    order.status = True
    order.save()

    return redirect('index')

def deleteorder(request, order_id):
    order= Order.objects.get(pk=order_id)
    order.delete()
    return redirect('payment')

def formpayment(request):
    return render(request,'main/formpayment.html')

