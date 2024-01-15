from django.shortcuts import render, HttpResponse,redirect,get_object_or_404,reverse

from .models import Contact
from django.contrib import messages

# Create your views here.
def contact_us(request):
    return render(request, 'Main/contact_us.html')


def addContact(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if full_name=="" or email=='' or message=='':
            messages.warning(request, "All fields Required")
            return redirect('/contact_us')

        else:
            newContact = Contact(full_name=full_name, email=email, message=message)
            newContact.save()
            messages.success(request, "Message Sent Successfully.")
            return redirect('/contact_us')