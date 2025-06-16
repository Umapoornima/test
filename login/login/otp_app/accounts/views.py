import random
import requests
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_msg91(mobile_number, otp):
    url = "https://control.msg91.com/api/v5/otp"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "authkey": os.getenv("MSG91_AUTH_KEY"),
        "template_id": os.getenv("MSG91_TEMPLATE_ID"),
        "mobile": f"91{mobile_number}",
        "otp": otp
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mobile_number = data.get("mobile")

        if not mobile_number:
            return JsonResponse({"error": "Mobile number is required"}, status=400)

        otp = generate_otp()
        response = send_otp_via_msg91(mobile_number, otp)

        request.session["otp"] = otp
        request.session["mobile"] = mobile_number

        return JsonResponse({"message": "OTP sent successfully", "msg91_response": response})

    return JsonResponse({"error": "Invalid request method"}, status=405)
