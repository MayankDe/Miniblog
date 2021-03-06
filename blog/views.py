from django.contrib import auth
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import Group
from django.http.request import host_validation_re
from django.shortcuts import redirect, render,HttpResponseRedirect

from . forms import LoginForm, SignUpForm,PostForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})
   


def about(request):
    return render(request,'blog/about.html')

def contact(request):
    return render(request,'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-id')
        #print(posts)
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_signup(request):
    if request.method == "POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            
            messages.success(request,'Congratulation! You are Registered Here.')
       
           
            form.save()
           
    else:
        form=SignUpForm() 
    return render(request,'blog/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                
                upass=form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in successfully !!....')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
            
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title,desc=desc)
                pst.save()
                form = PostForm
                messages.success(request,"Your post is save successfully")
                return redirect('dashboard')
        else:
            form = PostForm()
        return render(request,'blog/addpost.html',{'form':form})
          
    else:
        HttpResponseRedirect('/login/')

def update_post(request,id):
    print(id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request,'blog/addpost.html',{'form':form})
          
    else:
        HttpResponseRedirect('/login/')
    

def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)

            pi.delete()
            
            
            
            return HttpResponseRedirect('/dashboard/') 
    else:
        HttpResponseRedirect('/login/')

