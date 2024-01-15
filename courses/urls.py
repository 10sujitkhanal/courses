from django.urls import path, include
from .views import courses, filter_course, search_course, course_detail


urlpatterns = [
    path('',courses,name='courses'),
    path('<slug:slug>/',course_detail, name="course_detail"),
    path('filter-course',filter_course,name="filter-course"),
    path('search',search_course,name='search_course'),
    
]
