from django.db import models
from category.models import Categories
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    # user = models.OneToOne
    author_profile = models.ImageField(upload_to="author")
    name = models.CharField(max_length=100, null=True)
    skills = models.CharField(max_length=100, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name
    
class Level(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Language(models.Model):
    language = models.CharField(max_length=100)
    def __str__(self):
        return self.language


class Course(models.Model):
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )
    CERTIFICATE_STATUS = (
        ('YES','YES'),
        ('NO', 'NO'),
    )

    featured_image = models.ImageField(upload_to="featured_img",null=True)
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    level = models.ForeignKey(Level,on_delete=models.CASCADE, null=True)
    language = models.ForeignKey(Language,on_delete=models.CASCADE, null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    deadline = models.DateField(null=True)
    certificate = models.CharField(choices=CERTIFICATE_STATUS,max_length=100,null=True)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_detail", kwargs={'slug': self.slug})
    
    def get_all_review(self):
        reviews = ReviewRating.objects.filter(course__slug=self.slug).order_by("-id")
        return reviews
    
    def review_rating_count(self):
        reviews = ReviewRating.objects.filter(course__slug=self.slug).count()
        return reviews
    
    def review_rating_percentage(self):
        try:
            review = ReviewRating.objects.filter(course__slug=self.slug)
            average_rating = 0
            for r in review:
                average_rating += r.rating
            total_review = (average_rating/(review.count()*5))*100
        except:
            total_review=0
        return total_review
    
    def review_rating_average(self):
        try:
            review = ReviewRating.objects.filter(course__slug=self.slug)
            average_rating = 0
            for r in review:
                average_rating += r.rating
            total_review = (average_rating/review.count())
        except:
            total_review=0
        return total_review
    
    def lesson_count(self):
        return Lesson.objects.filter(course__slug=self.slug).count()
    
    def video_time_count(self):
        return Video.objects.filter(course__slug=self.slug).aggregate(sum=Sum('time_duration'))

    def author_total_course(self):
        return Course.objects.filter(author=self.author).count()



def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)


class WhatYouLearn(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE,)
    points = models.CharField(max_length=500)
    
    def __str__(self):
        return str(self.course) + " " + str(self.points)


class Requirements(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE,)
    points = models.CharField(max_length=500)
    
    def __str__(self):
        return str(self.course) + " " + str(self.points)
    
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.course) + " - " + str(self.name)
    
class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="video/thumbnail", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)
    youtube_id = models.CharField(max_length=100)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class ReviewRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.review
    