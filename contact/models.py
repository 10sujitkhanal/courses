from django.db import models

# Create your models here.
class Contact(models.Model):
    full_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 200)
    message = models.CharField(max_length= 500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    class Meta:
        ordering = ['-date']