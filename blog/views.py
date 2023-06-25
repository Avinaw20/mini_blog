from django.shortcuts import render,HttpResponsePermanentRedirect, redirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
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
        posts = Post.objects.all()
        return render(request,'blog/dashboard.html',{'posts':posts})
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
            user = form.save()
            
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


def add_post(request):
    if request.user.is_authenticated:
        form = PostForm()  # Set a default form instance

        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                form = PostForm()  # Reset the form after saving the post

        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponsePermanentRedirect('/login/')

    
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk = id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk = id)
            form = PostForm(instance=pi)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponsePermanentRedirect('/login/')

def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk = id)
            pi.delete()
            return HttpResponsePermanentRedirect('/dashboard/')
    else:
        return HttpResponsePermanentRedirect('/login/')