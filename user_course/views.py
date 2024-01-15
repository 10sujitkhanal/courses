from django.shortcuts import render
from user_course.models import UserCourse

# Create your views here.
def mycourses(request):
    course = UserCourse.objects.filter(user=request.user)
    context = {
        'course':course,
    }
    return render(request,'user_courses/mycourse.html',context)