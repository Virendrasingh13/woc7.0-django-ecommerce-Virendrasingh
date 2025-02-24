from cmath import log
from tkinter import E
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
from .models import Profile 
from base.emails import send_account_activation_email
import uuid
from products.models import Product
from accounts.models import *
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


#razor
import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from accounts.models import Cart  

from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt



def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()
        

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/register.html')




def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')
    
@login_required
def profile_page(request):
    profile = request.user.profile  # Fetch the profile
    return render(request , 'accounts/profile.html',{"profile": profile})

def logout_page(request):
    logout(request)
    return redirect('/')

@login_required
def cart_page(request):
    cart = Cart.objects.filter(is_paid=False, user=request.user).first()  # Get the latest unpaid cart
    cart_items = CartItem.objects.filter(cart=cart).select_related('product').prefetch_related('product__product_images')  
    context = {'cart': cart, 'cart_items': cart_items}
    return render(request, 'accounts/cart.html', context)

@login_required
def add_to_cart(request, uid):
    product = Product.objects.get(uid = uid)
    user = request.user
    cart , _ = Cart.objects.get_or_create(user = user , is_paid = False)
    cart_items = CartItem.objects.create(cart = cart , product = product )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def remove_cart(request, cart_item_uid):
    cart_item = get_object_or_404(CartItem, uid=cart_item_uid)  # Fetch or return 404
    cart_item.delete()  # Delete the cart item
    return redirect(request.META.get('HTTP_REFERER', 'cart'))  # Redirect back to cart page


@csrf_exempt
def payment_success(request):
    cart = Cart.objects.get(user=request.user, is_paid=False)
    cart.is_paid = True  # Mark cart as paid
    cart.save()
    return redirect("cart")  # Redirect to cart or success page



def create_razorpay_order(request):
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user, is_paid=False)
        total_price = cart.get_cart_total() * 100  # Razorpay takes amount in paise (1 INR = 100 paise)
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment_data = {
            "amount": total_price,
            "currency": "INR",
            "payment_capture": 1  # Auto capture payment
        }
        order = client.order.create(data=payment_data)

        return JsonResponse(order)  # Return order details as JSON


#order

from django.shortcuts import render, redirect
from accounts.models import Order, Cart
import razorpay

def create_razorpay_order(request):
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user, is_paid=False)
        total_price = cart.get_cart_total() * 100  # Razorpay takes amount in paise

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment_data = {
            "amount": total_price,
            "currency": "INR",
            "payment_capture": 1  # Auto capture payment
        }
        order = client.order.create(data=payment_data)

        return JsonResponse(order)  # Return order details as JSON
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        try:
            cart = Cart.objects.get(user=request.user, is_paid=False)
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Cart not found"}, status=400)

        # Mark cart as paid
        cart.is_paid = True
        cart.save()

        # Create order record
        Order.objects.create(
            user=request.user,
            cart=cart,
            razorpay_order_id=order_id,
            razorpay_payment_id=payment_id,
            razorpay_signature=signature,
            is_paid=True
        )

        return JsonResponse({"success": True, "message": "Payment successful!"})

    return JsonResponse({"error": "Invalid request method"}, status=400)


def orders_page(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "accounts/orders.html", {"orders": orders})
