from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from category.models import Categories
from courses.models import Course
from blog.models import Post

# Create your views here.
def BASE(request):
    return render(request, 'base/base.html')

def home(request):
    categories = Categories.objects.all().order_by('id')[0:5]
    courses = Course.objects.filter(status="PUBLISH").order_by('-id')
    posts = Post.objects.all().order_by('-id')[0:4]

    context = {
        'category':categories,
        'course':courses,
        'posts':posts,
    }
    return render(request, 'Main/home.html', context)

def about_us(request):
    return render(request, 'Main/about_us.html')

def profile(request):
    return render(request, 'profile/profile.html')

def Profile_Update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('profile')