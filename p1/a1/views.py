from django.shortcuts import render,redirect,get_object_or_404
from .models import user
# def reg(req):
#     if req.method == "POST":
#         name = req.POST.get('name')
#         email = req.POST.get('email')
#         password = req.POST.get('password')
#         u = user(name=name,email=email,password=password)
#         u.save()
#         return redirect('success')
#     else:
#         return render(req,'reg.html')
import random
from django.core.mail import send_mail
from django.conf import settings

def reg(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')


        otp = random.randint(100000, 999999)

        request.session['reg_data'] = {
            'name': name,
            'email': email,
            'password': password
        }
        request.session['otp'] = otp

        send_mail(
            'Your OTP Code',
            f'Your OTP is {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return redirect('verify_otp')

    return render(request, 'reg.html')

def success(req):
    return render(req,'success.html')

def dash(abc):
    users = user.objects.all()
    return render(abc,'dash.html',{'user':users})

def update_user(request, id):
    u = get_object_or_404(user, id=id)

    if request.method == "POST":
        u.name = request.POST.get('name')
        # u.email = request.POST.get('email')
        u.password = request.POST.get('password')
        u.save()
        return redirect('dash')

    return render(request, 'update.html', {'u': u})

def delete_user(request, id):
    u = get_object_or_404(user, id=id)
    u.delete()
    return redirect('dash')

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if str(session_otp) == entered_otp:
            data = request.session.get('reg_data')

            u = user(
                name=data['name'],
                email=data['email'],
                password=data['password']
            )
            u.save()


            request.session.flush()

            return redirect('success')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html')

# Create your views here.
