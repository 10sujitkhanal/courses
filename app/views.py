from django.shortcuts import render, redirect

def home(request):
    return render(request, 'Main/home.html')

def single_course(request):
    return render(request, 'Main/single_course.html')

def contact_us(request):
    return render(request, 'Main/contact_us.html')

def about_us(request):
    return render(request, 'Main/about_us.html')

def PAGE_NOT_FOUND(request, exception):
    return render(request,'error/404.html')
