from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from main.models import *
# Create your views here.
@login_required
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
            context['error'] = 'ชื่อผู้ใช้ หรือ รหัสผ่านผิด โปรดลองอีกครั้ง'
    return render(request,'login_page.html',context=context)
def my_logout(request):
    logout(request)
    return redirect('login')
def my_register(request):
    if request.method == 'POST':
        username = request.POST['u_name']
        firstname = request.POST['f_name']
        lastname = request.POST['l_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
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
                user.save()
                return redirect('login')
        else:
            messages.info(request,'รหัสผ่านไม่ตรงกัน')
            return redirect('register')
    return render(request,template_name='register_page.html')