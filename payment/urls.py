from django.urls import path, include
from .views import success_payment


urlpatterns = [
    path('<slug:order_id>/',success_payment, name="success_payment"),
    
]
