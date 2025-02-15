from pydoc import render_doc
from tkinter import E
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from products.models import Product



def get_product(request , slug):
    try:
        product = Product.objects.get(slug =slug)
        return render(request  , 'product/product.html' , context = {'product' : product})

    except Exception as e:
        print(e)


