from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from category.models import Categories
from courses.models import Course, Level, Video, ReviewRating
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from user_course.models import UserCourse



def courses(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price=0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    
    context = {
        'category':category,
        'level':level,
        'course':course,
        'FreeCourse_count':FreeCourse_count,
        'PaidCourse_count':PaidCourse_count
    }
    return render(request, 'courses/course.html', context)

def filter_course(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    
    
    if 'query' in request.GET:
        query = request.GET['query']
        course = Course.objects.filter(title__icontains = query)
    else:
        course = Course.objects.all().order_by('-id')

    if price == ['pricefree']:
       course = course.filter(price=0)
    if price == ['pricepaid']:
       course = course.filter(price__gte=1)
    if price == ['priceall']:
       course = course.all()
    if categories:
       course = course.filter(category__id__in=categories).order_by('-id')
    if level:
       course = course.filter(level__id__in = level).order_by('-id')


    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})

def search_course(request):
    if 'query' in request.GET:
        query = request.GET['query']
        course = Course.objects.filter(title__icontains = query)
        FreeCourse_count = course.filter(price=0).count()
        PaidCourse_count = course.filter(price__gte=1).count()
        level = Level.objects.all()
        context = {
            'level':level,
            'course':course,
            'query': query,
            'FreeCourse_count':FreeCourse_count,
            'PaidCourse_count':PaidCourse_count
        }
        return render(request,'search/search.html',context)
    else:
        return redirect('courses')
    

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    related_course = Course.objects.filter(category=course.category)
    latest_course = Course.objects.all().order_by('-id')[0:5]
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    reviews = ReviewRating.objects.filter(course__id=course.id, status=True)
    total_student_enroll = UserCourse.objects.filter(course__author=course.author).values('user').distinct().count()
    total_course_review = ReviewRating.objects.filter(course__author=course.author).count()
    if request.user.is_authenticated:
        try:
            check_enroll =  UserCourse.objects.get(user=request.user, course=course)
        except UserCourse.DoesNotExist:
            check_enroll = None
    else:
        check_enroll = None
    context = {
        'course': course,
        'time_duration':time_duration,
        'check_enroll':check_enroll,
        'related_course':related_course,
        'latest_course':latest_course,
        'reviews':reviews,
        'total_student_enroll':total_student_enroll,
        'total_course_review':total_course_review,
    }
    return render(request,'courses/course_details.html', context)