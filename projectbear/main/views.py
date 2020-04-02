from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
# Create your views here.
@login_required
def index(request):
    return HttpResponse('Index มาแล้ว')
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
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            user = User.objects.create_user(
                username = request.POST['u_name'],
                first_name = request.POST['f_name'],
                last_name = request.POST['l_name'],
                email = request.POST['email'],
                password = request.POST['password1'],
            )
            user.save()
            return redirect('login')
        else:
            return redirect('register')
    return render(request,template_name='register_page.html')