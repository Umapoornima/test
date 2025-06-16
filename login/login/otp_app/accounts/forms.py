from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=15)


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
