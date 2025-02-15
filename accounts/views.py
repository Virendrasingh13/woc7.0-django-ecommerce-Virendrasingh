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
from accounts.models import Cart,CartItem
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


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
