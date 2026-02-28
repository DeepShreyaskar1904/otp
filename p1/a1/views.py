from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from captcha.models import CaptchaStore
import random
from .models import *

def reg(request):

    if request.method == "GET":
        hashkey = CaptchaStore.generate_key()
        captcha_image_url = f"/captcha/image/{hashkey}/"

        return render(request, "reg.html", {
            "captcha_key": hashkey,
            "captcha_image": captcha_image_url
        })

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user_captcha = request.POST.get("captcha")
        captcha_key = request.POST.get("captcha_key")

        captcha_valid = CaptchaStore.objects.filter(
            hashkey=captcha_key,
            response=user_captcha
        ).exists()

        if not captcha_valid:
            hashkey = CaptchaStore.generate_key()
            captcha_image_url = f"/captcha/image/{hashkey}/"

            return render(request, "reg.html", {
                "error": "Invalid captcha",
                "captcha_key": hashkey,
                "captcha_image": captcha_image_url
            })

        otp = random.randint(100000, 999999)

        request.session["reg_data"] = {
            "name": name,
            "email": email,
            "password": password
        }
        request.session["otp"] = otp

        send_mail(
            "Your OTP Code",
            f"Your OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return redirect("verify_otp")

def verify_otp(request):

    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if str(session_otp) == entered_otp:

            data = request.session.get('reg_data')

            user = User.objects.create_user(
                username=data['email'],   # using email as username
                email=data['email'],
                password=data['password'],
                first_name=data['name']
            )

            login(request, user)   # auto login

            request.session.pop('otp', None)
            request.session.pop('reg_data', None)

            return redirect(login_view)

        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html')

def login_view(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dash')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# @login_required(login_url='login')
def dash(abc):
    users = user.objects.all()
    # for u in users:
    #     u.password = make_password(u.password)
    return render(abc,'dash.html',{'user':users})
@login_required(login_url='login')
def update_user(request, id):
    u = get_object_or_404(User, id=id)

    if request.method == "POST":
        u.first_name = request.POST.get('name')
        new_password = request.POST.get('password')

        if new_password:
            u.set_password(new_password)

        u.save()
        return redirect('dash')

    return render(request, 'update.html', {'u': u})

@login_required(login_url='login')
def delete_user(request, id):
    u = get_object_or_404(User, id=id)
    u.delete()
    return redirect('dash')

def success(req):
    return render(req,'success.html')