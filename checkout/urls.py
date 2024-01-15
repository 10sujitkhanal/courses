from django.urls import path, include
from .views import checkout, verify_payment


urlpatterns = [
    path('<slug:slug>/',checkout, name="checkout"),
    path('api/verify_payment',verify_payment,name='verify_payment')
    
]
