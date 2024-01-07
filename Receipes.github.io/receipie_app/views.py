from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 
# Create your views here.

@login_required(login_url='/login/')
def receipes(request):
    if request.method == "POST":
      data = request.POST
      receipe_image = request.FILES.get('receipe_image')
      receipe_name = data.get('receipe_name')
      receipe_description  = data.get('receipe_description')
    #  print(ereipie_description) 
    #  print(receipe_name) 
    #  print(receipe_image) 
    # print(data)
      Receipe.objects.create(
        receipe_name = receipe_name,
        receipe_description = receipe_description,
        receipe_image = receipe_image,
      )
      return redirect('/receipe/')
    

       
    queryset = Receipe.objects.all()
    if request.GET.get('search'):
      #  print(request.GET.get('search'))
      queryset = queryset.filter(recipie_name__icontains = request.GET.get('search'))

    context = {'receipes':queryset}
    return render(request,'home/receipies.html',context)

@login_required(login_url='/login/')
def update_receipe(request, id):
   queryset = Receipe.objects.get(id=id)

   if request.method == "POST":
      data = request.POST
      receipe_image = request.FILES.get('receipe_image')
      receipe_name = data.get('receipe_name')
      receipe_description  = data.get('receipe_description')

      queryset.receipe_name = receipe_name
      queryset.receipe_description = receipe_description
      if receipe_image:
         queryset.receipe_image = receipe_image
      
      queryset.save()
      return redirect('/receipe/')
   
   context = {'receipe':queryset}
   return render(request,'home/update_receipes.html',context)

@login_required(login_url='/login/')
def delete_receipe(request, id):
   queryset = Receipe.objects.get(id=id)
   queryset.delete()
   return redirect('/receipe/')
def login_page(request):
   if request.method=="POST":
      username = request.POST.get('username')
      password = request.POST.get('password')

      if not User.objects.filter(username=username).exists():
         messages.info(request,'Invalid Username or password')
         return redirect('/login/') 

      user = authenticate(username = username, password = password)

      if user is None:
         messages.error(request,'Invalid Username or password')   
         return redirect('/login/') 
      else:
         login(request,user)
         return redirect('/receipe/')
      
   return render(request,'home/login.html')

def logout_page(request):
   logout(request)
   return redirect('/login/')

def register_page(request):
   if request.method=="POST":
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      username = request.POST.get('username')
      password = request.POST.get('password')

      user = User.objects.filter(username=username)

      if user.exists():
         messages.info(request,'Username already taken')
         return redirect('')
     
      user = User.objects.create(
         first_name=first_name,
         last_name=last_name,
         username=username
      )
      user.set_password(password)
      user.save()

      messages.info(request,'Account created successfully')

      return redirect('/register/')
   return render(request,'home/register.html')