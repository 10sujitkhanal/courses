from django.urls import path
from . import views

urlpatterns = [
    path('submit_review/<slug:slug>/', views.submit_review, name='submit_review'),
]