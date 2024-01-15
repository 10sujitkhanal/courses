from django.shortcuts import render, redirect, get_object_or_404
from courses.models import ReviewRating
from django.contrib import messages
from courses.models import Course

# Create your views here.
def submit_review(request, slug):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_content = request.POST.get('review')
        try:
            reviews = ReviewRating.objects.get(user=request.user, course__slug=slug)
            reviews.rating = rating
            reviews.review = review_content
            reviews.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url+"#review_rating_content")
        except:
            course = get_object_or_404(Course, slug=slug)
            reviews = ReviewRating.objects.create(rating=rating,review=review_content, course=course, user=request.user)
            messages.success(request, 'Thank you! Your review has been submitted.')
            return redirect(url+"#review_rating_content")
            