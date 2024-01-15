from django.shortcuts import render
from .models import Payment
from django.shortcuts import get_object_or_404

# Create your views here.
def success_payment(request, order_id):
    payment = get_object_or_404(Payment, order_id=order_id)
    context = {
        'payment':payment,
    }
    return render(request,'payment/success.html',context)