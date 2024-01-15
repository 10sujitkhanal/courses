from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# Create your models here.
class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.first_name) + " - " + str(self.course.title)