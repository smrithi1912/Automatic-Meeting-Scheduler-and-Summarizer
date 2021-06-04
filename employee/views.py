from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import employee,meeting,Meets
from django import forms
from django.db.models import F
from .forms import Scheduler
from django.http import HttpResponseRedirect
# Create your views here
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            employee.objects.create(name=username)
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            print("yaaa!")
            return redirect("../upload/")
        else:    
            password1 = form.data['password1']
            password2 = form.data['password2']
            for msg in form.errors.as_data():
                if msg == 'email':
                    messages.error(request, f"Declared {email} is not valid")
                if msg == 'password2' and password1 == password2:
                    messages.error(request, f"Selected password: {password1} is not strong enough")
                elif msg == 'password2' and password1 != password2:
                    messages.error(request,
                                   f"Password: '{password1}' and Confirmation Password: '{password2}' do not match")
                else:
                    messages.error(request,
                                   f"Error")
    form = UserCreationForm
    return render(request=request,
                  template_name="employee/register.html",
                  context={"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("../welcome/")


def login_request(request):
    if request.user.is_authenticated:
        return redirect('../dashboard/1/')
    if request.method == 'GET':
        print('fneriu44')
        form = AuthenticationForm()
        return render(request, 'employee/login.html', {'form': form})
    if request.method == 'POST':
        print("egniurnbriubnrtbuirnbruibnrsbrs")
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('../dashboard/1/')
            else:
                print("Can i get a hooyaa")
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm(data=request.POST)
    return render(request,
                  "employee/login.html",
                  {"form": form})

def profile_view(request, id):
    obj = employee.objects.get(id=id)
    context = {
        "con": obj,
    }
    return render(request, "employee/profile.html", context)
    
def dashboard_view(request,id):
    if request.user.is_authenticated is True:
        if request.user.id is id:
            obj = employee.objects.get(id=id)
            all_meets = obj.meetings.values()
            context={
                "con":obj,
                "all": all_meets,
            }
            return render(request,"employee/dashboard.html",context)
        else:
            return redirect(dashboard_view,request.user.id)
    else:
        return redirect(register_view)
def schedule_view(request,id):
    if request.user.is_authenticated is True:
        if request.user.id is id:
            obj= employee.objects.get(id=id)
            all_meets = obj.meetings.values()
            context = {
                "con": obj,
                "all": all_meets,
            }
            return render(request,"employee/schedule.html",context)
        else:
            return redirect(schedule_view,request.user.id)
    else:
        return redirect(register_view)
from django.conf import settings
from django.core.mail import send_mail

def scheduler_view(request,id):
    if request.user.is_authenticated is True:
        if request.user.id is id:
            context ={}  
            if request.method == 'GET':
                form=Scheduler()
            # create object of form
            else:
                form = Scheduler(request.POST)  
                # check if form data is valid
                if form.is_valid():
                    # save the form data to model
                    t=form.cleaned_data.get('title')
                    st=form.cleaned_data.get('start_time')
                    et=form.cleaned_data.get('end_time')
                    p=form.cleaned_data.get('participants')
                    l= form.cleaned_data.get('link')
                    # email=form.cleaned_data.get('email_id_of_participants')
                    # email_list= email.split (",")
                    new_meeting=meeting(title=t,start_time=st,end_time=et,link=l)           
                    for i in p:
                        through_table=Meets(m=new_meeting,e=i)
                    subject = 'Invitation for a meeting'
                    message = f'You have been invited for a meeting at {new_meeting.start_time} about {new_meeting.title} and here is the link {new_meeting.link}.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list=[]
                    # for i in email_list:
                    #     recipient_list.append(i)
                    # print(recipient_list)
                    for i in p:
                        recipient_list.append(i.email_id)
                    send_mail( subject, message, email_from, recipient_list )
                    form.save()  
                    return redirect(dashboard_view,id)
            context['form']= form
            return render(request, "employee/scheduler.html", context)
        else:
            return redirect(scheduler_view,request.user.id)
    else:
        return redirect(register_view)




