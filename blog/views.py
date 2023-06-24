from django.shortcuts import render,HttpResponsePermanentRedirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,'blog/home.html')


def about(request):
    return render(request,'blog/about.html')

def contact(request):
    return render(request,'blog/contact.html')

def dashboard(request):
    return render(request,'blog/dashboard.html')

def user_logout(request):
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
    form = LoginForm()
    return render(request,'blog/login.html',{'form':form})