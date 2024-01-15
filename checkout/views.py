from django.shortcuts import render, redirect
from courses.models import Course
from user_course.models import UserCourse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import requests
import json 
from django.http import JsonResponse
import urllib.parse
from payment.models import Payment


# Create your views here.
@csrf_exempt
def checkout(request, slug):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, slug=slug)
        try:
            check_enroll =  UserCourse.objects.get(user=request.user, course=course)
        except UserCourse.DoesNotExist:
            check_enroll = None
        
        if request.method == "POST":
            payload_str = request.POST.get('payload')
            payload_str = json.loads(payload_str)
            
            form_data = request.POST.get('form_data')
            form_data_dict = urllib.parse.parse_qs(form_data)
            print(form_data_dict)
            
            payment_status = verify_payment(payload_str, form_data_dict).content.decode('utf-8')
            payment_status = json.loads(payment_status)
            
            if payment_status.get('status') == "true":
                full_name = f"{form_data_dict.get('first_name')[0]} {form_data_dict.get('last_name')[0]}"
                phone_number = form_data_dict.get('phone')[0]
                email = form_data_dict.get('email')[0]
                order_comment = form_data_dict.get('order_comments')[0]
                payment_type = form_data_dict.get('payment_method')[0]
                user_course = UserCourse(
                    user = request.user,
                    course = course,
                )
                user_course.save()
                payment = Payment(
                    full_name=full_name,
                    phone_number=phone_number,
                    email=email,
                    order_comment=order_comment,
                    payment_type=payment_type,
                    course = course,
                    user = request.user
                )
                payment.save()
                context = {
                    'payment':payment,
                }
                return JsonResponse({'status':'true','message':'Payment Successfull','payment':payment.order_id}, safe=False)
            
            else:
                return JsonResponse({'status':'false','message':'Payment Failed','payment':'error'}, status=500)

        
            
        if check_enroll == None:
            if course.price == 0:
                course = UserCourse(
                    user = request.user,
                    course = course,
                )
                course.save()
                messages.success(request, 'Course Are Successfully Enrolled...')
                return redirect('mycourses')
            else:
                context = {
                    'course':course,
                }
                return render(request,'checkout/checkout.html',context)
        else:
            messages.success(request, 'Course Already Enrolled...')
            return redirect('mycourses')
    else:
        return redirect('mycourses')

def verify_payment(payload_str,form_data_dict):
    try:
        payment_method = form_data_dict.get('payment_method')[0]
        if payment_method == "KHALTI":
            return khalti_payment(payload_str)
    except:
        return JsonResponse({'status':'false','message':'Something went wrong sujit'}, safe=False)
        
def khalti_payment(payload_str):
    token = payload_str['token']
    amount = payload_str['amount']
    
    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {"token": token,"amount": amount}
    headers = {"Authorization": "Key test_secret_key_3c9f39b029f7403e9d28aef58e3326bd"}
    
    response = requests.post(url, payload, headers = headers)
    response_data = json.loads(response.text)
    status_code = str(response.status_code)
    

    if status_code == '400':
        response = JsonResponse({'status':'false','message':response_data['detail']}, status=500)
        return response
    
    return JsonResponse({'status':'true','message':"Payment Successful"},safe=False)