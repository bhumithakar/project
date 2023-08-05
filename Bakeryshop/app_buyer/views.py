from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
import random
from .models import *
from app_seller.models import *
from app_buyer.models import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
def index(request):
    return render(request,"index.html")

def account(request):
    return render(request,"account.html")

def register(request):
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
            return render(request,"otp.html")
        else:
            return render(request,"register.html",{"msg":"Password And Confirm Password Not Match"})  
    else:    
        return render(request,"register.html")
    
def otp(request):    
    if request.method=="POST":
        if otp==int(request.POST["otp"]):
            User.objects.create(
                name=temp["name"],
                email=temp["email"],
                password=make_password(temp["password"])

            )
            return render(request,"register.html",{"msg":"registration successfull"})
        else:
            return render(request,"otp.html",{"msg":"otp not matched"})

    else: 
        return render(request,"register.html",{"msg":"You can not access direct otp please enter correct password and email"})
    
def login(request):
    if request.method=="POST":
        try:
            user_data=User.objects.get(email=request.POST["email"])
            if check_password(request.POST["password"],user_data.password):
                request.session["email"]=request.POST["email"]
                return render(request,"index.html")
            else:
                return render(request,"login.html",{"msg":"Password Not Match"})
        except:
            return render(request,"login.html",{"msg":"User not Exist"})

    else:
        return render(request,"login.html")
    
def logout(request):
    del request.session["email"]
    return render(request,"login.html",{"msg":"Logout Successfully"})

def profile(request):
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
                    return render(request,"profile.html",{"data":data,"msg":"Profile Update Successfully"})
                else:
                    return render(request,"profile.html",{"data":data,"msg":"New Password And Confirm New Password Not Match"})
            else:
                return render(request,"profile.html",{"data":data,"msg":"Old Password Not Match"})
        else:
            data.name=request.POST["name"]
            data.propic=image_val
            data.save()
            return render(request,"profile.html",{"data":data,"msg":"Profile Update Successfully"})
    else:
        data=User.objects.get(email=request.session["email"])
        return render(request,"profile.html",{"data":data})

def show_product(request):
    all_product=Product.objects.all()
    return render(request,"shop.html",{"all_product":all_product})

def single_product(request,pk):
     one_product=Product.objects.get(id=pk)
     return render(request,"shop-details.html",{"one_product":one_product})

def add_to_cart(request,pk):
    data=User.objects.get(email=request.session["email"])
    try:
        exists_data=Cart.objects.get(Q(prd_id=pk) & Q(buyer_id=data.id))
        exists_data.qty+=1
        exists_data.save()
        return single_product(request,pk)
    except:
        product=Product.objects.get(id=pk)
        Cart.objects.create(
            prd_id=product,
            buyer_id=data,
            qty=1
        )
        return single_product(request,pk)