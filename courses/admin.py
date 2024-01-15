from django.contrib import admin
from .models import Author, Course, Level, WhatYouLearn, Requirements, Video, Lesson, Language, ReviewRating

class WhatYouLearnTabularInline(admin.TabularInline):
    model = WhatYouLearn
    
class RequirementsTabularInline(admin.TabularInline):
    model = Requirements
    
class VideoTabularInline(admin.TabularInline):
    model = Video

class LessonTabularInline(admin.TabularInline):
    model = Lesson
    
class CourseAdmin(admin.ModelAdmin):
    inlines = (WhatYouLearnTabularInline,RequirementsTabularInline, LessonTabularInline, VideoTabularInline)

admin.site.register(Author)
admin.site.register(Course, CourseAdmin)
admin.site.register(Level)
admin.site.register(Language)
admin.site.register(ReviewRating)