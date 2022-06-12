from django.shortcuts import render
from django.http.response import HttpResponse
from django.conf import Settings
from django.core.mail import EmailMessage, message
from django.core.mail import send_mail     # for the sending email funtionality
from django.conf import ENVIRONMENT_VARIABLE, settings
from .models import Appointment
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
import datetime

# Create your views here.

def home(request):
    return render(request, 'home.html', {})

class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST['fname']
        lname = request.POST['lname'] 
        email = request.POST['email']
        mob = request.POST['mob']
        ans = request.POST['ans']  # message request

        appointment = Appointment.objects.create(
            fname = fname,
            lname = lname,
            email = email,
            phone = mob,
            request = ans,
        )
        appointment.save()

        messages.add_message(request,messages.SUCCESS, f"Thank you {fname} {lname}. We will confirm you your appointment through your email: {email} soon!")
        return HttpResponseRedirect(request.path)



def manage_app(request):
    return render(request, 'manage_app.html', {})



def contact_us(request):
    # this is the contact us form in the bottom of home
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        send_mail(
            email,
            message,
            name,
            ['azu.dev.01@gmail.com'],
        )
        # print("success")
        # return render(request, 'contact_us.html')
        messages.add_message(request, messages.SUCCESS, f"Dear {name}, your request has been sent to us, we will get back to you through your email: '{email}' soon.")
        return HttpResponseRedirect(request.path)

    else:
        return render(request, 'contact_us.html', {})

# def createaccountpage(request):
#     user="none"
#     error=""
#     if request.method=='POST':
#         name=request.POST['name']
#         email=request.POST['email']
#         password=request.POST['password']
#         requestpassword= request.POST['repeatpassword']
#         gender= request.POST['gender']
#         address=request.POST['address']
#         phonenumber=request.POST['phonenumber']
#         birthdate=request.POST['dateofbirth']
#         bloodgroup=request.POST['bloodgroup']

#         try:
#             if password==repeatpassword:
#                 Patient.objects.create(name=name,email=email, gender=gender,address=address,phonenumber=phonenumber,birthdate=birthdate,bloodgroup=bloodgroup)
#                 user=User.objects.create_user(first_name=name,email=email, password=password, username=email)
#                 pat_group=Group.objects.get(name='Patient')
#                 pat_group.user_set.add(user)
#                 user.save()
#                 error="no"
#             else:
#                 error="yes"
    
#         except Exception as e:
#             error="yes"
#     d= {'error': error}

#     return render(request,'createaccount.html',d)
       

def appointment_succ(request):
    return render(request, 'appointment_succ.html', {})



class ManageAppointmentTemplateView(TemplateView):
    template_name = "manage_app.html"
    model = Appointment
    login_required = True   # so not everyone can access the manage page
    
    def post(self, request):
        date= request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id= appointment_id)
        appointment.accepted = True
        appointment.accepted_date = datetime.datetime.now()
        appointment.save()

        info = {
            "fname" : appointment.fname,
            "lname" : appointment.lname,
            "date" : date,
        }
        message = get_template('email.html').render(info)

        email= EmailMessage(
            "Appointment confirmation at Health Support DJP System",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
        )
        email.content_subtype= "html"
        email.send()

        messages.add_message(request, messages.SUCCESS, f"Patient {appointment.fname}'s appointment has been set for {date}")
        return HttpResponseRedirect(request.path)



    # in order to send some extra data form the template to the view we write get_context_data ()
    def get_context_data(self, *args, **kwargs):   
        context= super().get_context_data(*args, **kwargs)
        appointment= Appointment.objects.all()

        context.update({
            "appointment" : appointment,
            "title" : "Manage Appointments"
        })
        return context










        
        

