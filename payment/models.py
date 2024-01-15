from django.db import models
from courses.models import Course
from user_course.models import UserCourse
from django.contrib.auth.models import User
import uuid

PAYMENT_TYPE = (
        ('KHALTI','KHALTI'),
        ('ESEWA', 'ESEWA'),
    )
# Create your models here.
class Payment(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    payment_id = models.CharField(max_length=200,null=True, blank=True)
    full_name = models.CharField(max_length=200,null=True)
    phone_number = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    order_comment = models.CharField(max_length=500,null=True)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(choices=PAYMENT_TYPE,max_length=100,null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
    

    def __str__(self):
        return f'{self.order_id} --- {self.user.first_name} {self.user.last_name} --- {self.course}'