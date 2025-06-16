from django.shortcuts import render, redirect
from .forms import UserForm, OTPForm
from .models import UserOTP
import random
from twilio.rest import Client
import random


def send_otp(mobile):
    otp = str(random.randint(100000, 999999))
    print(f"Sending OTP {otp} to {mobile}")
    return otp


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            mobile = form.cleaned_data['mobile']
            otp = send_otp(mobile)
            UserOTP.objects.create(username=username, mobile=mobile, otp=otp)
            request.session['mobile'] = mobile
            return redirect('verify_otp')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


def verify_otp(request):
    mobile = request.session.get('mobile')
    if not mobile:
        return redirect('register')
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            user = UserOTP.objects.filter(mobile=mobile).last()
            if user and user.otp == entered_otp:
                return render(request, 'success.html', {'user': user})
            else:
                return render(request, 'verify_otp.html', {'form': form, 'error': 'Invalid OTP'})
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})
