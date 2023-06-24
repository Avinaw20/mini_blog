from django.shortcuts import render,HttpResponsePermanentRedirect, redirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import Post
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
        return render(request,'blog/dashboard.html')
    else:
        return HttpResponsePermanentRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponsePermanentRedirect('/')

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations !! You have become an Author.')
            form.save()
    else :
        form = SignUpForm()
    return render(request,'blog/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username = uname, password = upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged In successfully')
                    return HttpResponsePermanentRedirect('/dashboard/')
        else:
            form = LoginForm() 
        return render(request,'blog/login.html',{'form':form})
    else:# yaani pehle se login h to
        return HttpResponsePermanentRedirect('/dashboard/')