from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from gfg import settings

# Create your views here.

def home(request):
    return render(request,"authentication/index.html")

def signup(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        #checking if username already exists
        if User.objects.filter(username = username):
            messages.error(request,"username already exist! please try some other username")
        
        #checking if email exists
        if User.objects.filter(email = email).exists():
           messages.error(request,"Email already registered!") 
           return redirect('home')
       
        #making sure length of username less than 10
        if len(username)>10:
            messages.error(request,"username must be under 10 characters")
        
        #making sure pass1 = pass2
        if pass1 != pass2:
            messages.error(request,"passwords not matching ")
            
        #making sure username alphanumeric
        if not username.isalnum():
            messages.error(request,'username must be alphanumeric')
            return redirect('home')
        
        #getting data
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name=fname           #asking first name
        myuser.last_name=lname            #asking last name
        myuser.is_active = False
        
        #saving data
        myuser.save()
        
        #sending message
        messages.success(request,"your account has been successfully created")
        
        #redirects to login page
        return redirect("signin")
    
    # connects to signup webpage
    return render(request,"authentication/signup.html")

def signin(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")
        
        #to authenticate
        user = authenticate(username = username, password=pass1)
        
        #checking if user in dbms
        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request,"authentication/index.html",{'fname': fname})
        else:
            messages.error(request,"bad credentials!!")
            return redirect("home")
            
    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"logged out successfully!")
    return redirect('home')
