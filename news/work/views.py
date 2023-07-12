from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url=('/login/'))
def news_logic(request):
    if request.method == 'POST':
        data = request.POST
        news_img = request.FILES.get('news_img')
        news_name = data.get('news_name')
        news_desc = data.get('news_desc')
        news_date = data.get('news_date')

        News.objects.create(
            news_name = news_name,
            news_desc = news_desc,
            news_img = news_img,
            news_date = news_date,
        )
        messages.info(request,'News Added successfully')
        return redirect('/index/')
        
    queryset = News.objects.all()

    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
            Q(news_name__icontains = search)|
            Q(news_desc__icontains = search) |
            Q(news_date__icontains = search)
            )
        
    # paginator = Paginator(queryset, 5)  # Show 10 contacts per page.

    # page_number = request.GET.get("page",1)
    # page_obj = paginator.get_page(page_number)

    context = {'news_logic' : queryset}
    
    return render(request,'index.html',context)


@login_required(login_url=('/login/'))
def edit_news(request, id):
    queryset = News.objects.get(id = id)

    if request.method == 'POST':
        data = request.POST
        news_img = request.FILES.get('news_img')
        news_name = data.get('news_name')
        news_desc = data.get('news_desc')
        news_date = data.get('news_date')

        queryset.news_name = news_name
        queryset.news_desc = news_desc
        queryset.news_date = news_date

        if news_img:
            queryset.news_img = news_img
        
        queryset.save()
        messages.info(request,'News Updated successfully')
        return redirect('/index/')
    
    context = {'edit_news1' : queryset}
    return render(request,'edit_news.html',context)

@login_required(login_url=('/login/'))
def delete_news(request, id):
    queryset = News.objects.get(id = id)
    queryset.delete()
    messages.info(request,'News Deleted successfully')
    return redirect('/index/')

def register_page(request):
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request,'Username already taken')
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )

        user.set_password(password)
        user.save()

        messages.info(request,"You have been Registered Successfully")
        return redirect('/login/')
    
    return render(request,'register.html')

def login_page(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request,"Invalid Username")
            return redirect('/login/')
        
        user = authenticate(username = username, password=password)

        if user is None:
            messages.error(request,"Invalid Data")
            return redirect('/login/')
        else:
            login(request,user)
            messages.info(request,"Login Successfully Done")
            return redirect('/index/')
        
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

        
        

