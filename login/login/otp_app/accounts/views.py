from django.shortcuts import render, redirect
from .forms import UserForm, OTPForm
from .models import UserOTP
import random
import requests
import os


def send_otp(mobile):
    otp = str(random.randint(100000, 999999))

    # MSG91 API integration
    url = "https://control.msg91.com/api/v5/otp"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "authkey": os.getenv("MSG91_AUTH_KEY"),
        "template_id": os.getenv("MSG91_TEMPLATE_ID"),
        "mobile": f"91{mobile}",
        "otp": otp
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f"MSG91 Response: {response.status_code}, {response.text}")

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
            input_otp = form.cleaned_data['otp']
            try:
                user_otp = UserOTP.objects.filter(mobile=mobile).latest('id')
                if user_otp.otp == input_otp:
                    return render(request, 'success.html')
                else:
                    return render(request, 'verify.html', {'form': form, 'error': 'Invalid OTP'})
            except UserOTP.DoesNotExist:
                return redirect('register')
    else:
        form = OTPForm()
    return render(request, 'verify.html', {'form': form})
