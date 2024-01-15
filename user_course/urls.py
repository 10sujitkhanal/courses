from django.urls import path, include
from .views import mycourses


urlpatterns = [
    path('',mycourses, name="mycourses"),
    
]
