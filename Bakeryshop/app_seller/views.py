from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
import random

from .models import *
from app_buyer.models import *
# from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
def seller_index(request):
    return render(request,"seller_index.html")

def add_product(request):
    if request.method=="POST":
        seller_data=Seller_user.objects.get(email=request.session["email"])
        product.objects.create(
            pro_name=request.POST["pname"],
            pro_price=request.POST["pro_price"],
            pro_qty=request.POST["pro_qty"],
            pro_image=request.FILES["p_image"],
            pro_desc=request.POST["pro_desc"],
            seller_id=seller_data
        )
        return render(request,"add_product.html",{"msg":"Product Added Successfully"})
    else:
        return render(request,"add_product.html")
    
def view_product(request):
    seller_data=Seller_user.objects.get(email=request.session["email"])
    my_product=product.objects.filter(id=seller_data)
    return render(request,"my_product.html",{"my_product",my_product})

def seller_register(request):
    if request.method=="POST":
        if request.POST["password"]==request.POST["cpassword"]:
            global temp
            temp={ 
            "name":request.POST["name"],
            "email":request.POST["email"],
            "password":request.POST["password"]# pswd =sing-up.html se fild name hai

        }
            global otp
            otp=random.randint(100000,999999)
            subject = 'OTP Verification'
            message = f'Your OTP is. {otp} valid for 5 mintute only'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST["email"], ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,"seller_otp.html")
        else:
            return render(request,"seller_register.html",{"msg":"Password And Confirm Password Not Match"})  
    else:    
        return render(request,"seller_register.html")
    
def seller_otp(request):    
    if request.method=="POST":
        if otp==int(request.POST["otp"]):
            User.objects.create(
                name=temp["name"],
                email=temp["email"],
                password=make_password(temp["password"])

            )
            return render(request,"seller_register.html",{"msg":"registration successfull"})
        else:
            return render(request,"seller_otp.html",{"msg":"otp not matched"})

    else: 
        return render(request,"seller_register.html",{"msg":"You can not access direct otp please enter correct password and email"})
    
def seller_login(request):
    if request.method=="POST":
        try:
            user_data=User.objects.get(email=request.POST["email"])
            if check_password(request.POST["password"],user_data.password):
                request.session["email"]=request.POST["email"]
                return render(request,"seller_index.html")
            else:
                return render(request,"seller_login.html",{"msg":"Password Not Match"})
        except:
            return render(request,"seller_login.html",{"msg":"User not Exist"})

    else:
        return render(request,"seller_login.html")
    
def seller_logout(request):
    del request.session["email"]
    return render(request,"seller_login.html",{"msg":"Logout Successfully"})

def seller_profile(request):
    data=User.objects.get(email=request.session["email"])
    if request.method=="POST":
        try:
            image_val=request.FILES["propic"]
        except:
            image_val=data.propic
        if request.POST["oldpassword"]:
            if check_password(request.POST["oldpassword"],data.password):
                if request.POST["newpassword"]==request.POST["cnewpassword"]:
                    data.name=request.POST["name"]
                    data.password=make_password(request.POST["newpassword"])
                    data.propic=image_val
                    data.save()
                    return render(request,"seller_profile.html",{"data":data,"msg":"Profile Update Successfully"})
                else:
                    return render(request,"seller_profile.html",{"data":data,"msg":"New Password And Confirm New Password Not Match"})
            else:
                return render(request,"seller_profile.html",{"data":data,"msg":"Old Password Not Match"})
        else:
            data.name=request.POST["name"]
            data.propic=image_val
            data.save()
            return render(request,"seller_profile.html",{"data":data,"msg":"Profile Update Successfully"})
    else:
        data=User.objects.get(email=request.session["email"])
        return render(request,"seller_profile.html",{"data":data})
