
from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import Product

class Profile(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
    profile_image = models.ImageField(upload_to = 'profile')

    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid = False, cart__user = self.user ).count()


@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)

    def get_cart_total(self):
        cart_items = self.cartitems.all()
        return sum(cart_item.product.price for cart_item in cart_items if cart_item.product)

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    def get_product_price(self):
        return self.product.price if self.product else 0

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.uid} by {self.user.username}"
