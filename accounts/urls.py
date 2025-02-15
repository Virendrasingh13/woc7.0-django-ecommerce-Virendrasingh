from django.urls import path
from accounts.views import login_page,register_page , activate_email,profile_page,logout_page, cart_page,add_to_cart,remove_cart,create_razorpay_order,payment_success

urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('register/' , register_page , name="register"),
   path('profile/' , profile_page , name="profile"),
   path('logout/' , logout_page , name="logout"),
   path('cart/' , cart_page , name="cart"),
   path('add-to-cart/<uid>/' , add_to_cart , name="add_to_cart"),
   path('remove-cart/<cart_item_uid>/' , remove_cart , name="remove_cart"),
   path('activate/<email_token>/' , activate_email , name="activate_email"),
   path("create_razorpay_order/", create_razorpay_order, name="create_razorpay_order"),
   path("payment-success/", payment_success, name="payment_success"),

]
