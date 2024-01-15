from django import template
import math
from category.models import Categories
from courses.models import ReviewRating
register = template.Library()

@register.simple_tag
def discount_calculation(price,discount):
    if discount == None or discount == 0:
        return price
    sellprice = price
    sellprice = price - (price * discount/100)
    return math.floor(sellprice)

@register.simple_tag
def user_single_rating(slug, user):
        review = ReviewRating.objects.get(course__slug=slug, user=user)
        total_review = (review.rating/5)*100
        return total_review
